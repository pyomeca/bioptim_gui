import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/variables.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class BoundChart extends StatelessWidget {
  final DecisionVariableType decisionVariableType;
  final int variableIndex;
  final int dofIndex;

  const BoundChart({
    super.key,
    required this.decisionVariableType,
    required this.variableIndex,
    required this.dofIndex,
  });

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      Variable variable = decisionVariableType == DecisionVariableType.state
          ? data.phasesInfo[0].stateVariables[variableIndex]
          : data.phasesInfo[0].controlVariables[variableIndex];

      final List<List<double>> dataPointsMin = [];
      final List<List<double>> dataPointsMax = [];
      final List<List<double>> dataPointsInitGuess = [];

      for (int phaseIndex = 0; phaseIndex < data.nbPhases; phaseIndex++) {
        variable = decisionVariableType == DecisionVariableType.state
            ? data.phasesInfo[phaseIndex].stateVariables[variableIndex]
            : data.phasesInfo[phaseIndex].controlVariables[variableIndex];

        dataPointsMin.add(variable.bounds.minBounds[dofIndex]);
        dataPointsMax.add(variable.bounds.maxBounds[dofIndex]);
        dataPointsInitGuess.add(variable.initialGuess[dofIndex]);
      }

      final double minY = dataPointsMin
          .map((e) => e.reduce((min, element) => min < element ? min : element))
          .reduce((min, element) => min < element ? min : element);

      final double maxY = dataPointsMax
          .map((e) => e.reduce((max, element) => max > element ? max : element))
          .reduce((max, element) => max > element ? max : element);

      final double minYExtended = minY - (maxY - minY) * 0.1;
      final double maxYExtended = maxY + (maxY - minY) * 0.1;

      return Column(
        children: [
          Text(variable.name),
          Container(
            height: 200,
            width: 400,
            padding: const EdgeInsets.all(16.0),
            child: LineChart(
              LineChartData(
                  gridData: const FlGridData(show: true),
                  titlesData: const FlTitlesData(show: true),
                  borderData: FlBorderData(show: true),
                  minX: 0,
                  maxX: data.nbPhases.toDouble(),
                  minY: minYExtended,
                  maxY: maxYExtended,
                  lineBarsData: _buildPhaseLineChartBarDataBounds(dataPointsMin,
                          dataPointsMax, data.nbPhases.toDouble()) +
                      _buildPhaseLineChartBarDataInitGuess(
                          dataPointsInitGuess, data.nbPhases.toDouble())),
            ),
          )
        ],
      );
    });
  }
}

List<LineChartBarData> _buildPhaseLineChartBarDataBounds(
  List<List<double>> dataPointsMin,
  List<List<double>> dataPointsMax,
  double nbPhases,
) {
  List<LineChartBarData> ret = [];

  for (int phaseIndex = 0; phaseIndex < nbPhases; phaseIndex++) {
    final nbPoints = dataPointsMin[phaseIndex].length;
    if (nbPoints == 1) {
      // constant min
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMin[phaseIndex][0],
          phaseIndex + 1, dataPointsMin[phaseIndex][0], Colors.red));

      // constant max
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMax[phaseIndex][0],
          phaseIndex + 1, dataPointsMax[phaseIndex][0], Colors.blue));
    } else if (nbPoints == 2) {
      // linear min
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMin[phaseIndex][0],
          phaseIndex + 1, dataPointsMin[phaseIndex][1], Colors.red));

      // linear max
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMax[phaseIndex][0],
          phaseIndex + 1, dataPointsMax[phaseIndex][1], Colors.blue));
    } else if (nbPoints == 3) {
      // first min
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMin[phaseIndex][0],
          phaseIndex + 0.1, dataPointsMin[phaseIndex][0], Colors.red));

      // constant min
      ret.add(_buildLine(phaseIndex + 0.1, dataPointsMin[phaseIndex][1],
          phaseIndex + 0.9, dataPointsMin[phaseIndex][1], Colors.red));

      // last min
      ret.add(_buildLine(phaseIndex + 0.9, dataPointsMin[phaseIndex][2],
          phaseIndex + 1, dataPointsMin[phaseIndex][2], Colors.red));

      // first max
      ret.add(_buildLine(phaseIndex.toDouble(), dataPointsMax[phaseIndex][0],
          phaseIndex + 0.1, dataPointsMax[phaseIndex][0], Colors.blue));

      // constant max
      ret.add(_buildLine(phaseIndex + 0.1, dataPointsMax[phaseIndex][1],
          phaseIndex + 0.9, dataPointsMax[phaseIndex][1], Colors.blue));

      // last max
      ret.add(_buildLine(phaseIndex + 0.9, dataPointsMax[phaseIndex][2],
          phaseIndex + 1, dataPointsMax[phaseIndex][2], Colors.blue));
    }
  }

  return ret;
}

List<LineChartBarData> _buildPhaseLineChartBarDataInitGuess(
  List<List<double>> dataPointsInitGuess,
  double nbPhases,
) {
  List<LineChartBarData> ret = [];

  for (int phaseIndex = 0; phaseIndex < nbPhases; phaseIndex++) {
    final nbPoints = dataPointsInitGuess[phaseIndex].length;
    if (nbPoints == 1) {
      ret.add(_buildLine(
          phaseIndex.toDouble(),
          dataPointsInitGuess[phaseIndex][0],
          phaseIndex.toDouble() + 1,
          dataPointsInitGuess[phaseIndex][0],
          Colors.black));
    } else if (nbPoints == 2) {
      // linear
      ret.add(_buildLine(
          phaseIndex.toDouble(),
          dataPointsInitGuess[phaseIndex][0],
          phaseIndex + 1,
          dataPointsInitGuess[phaseIndex][1],
          Colors.black));
    } else if (nbPoints == 3) {
      // first
      ret.add(_buildLine(
          phaseIndex.toDouble(),
          dataPointsInitGuess[phaseIndex][0],
          phaseIndex + 0.1,
          dataPointsInitGuess[phaseIndex][0],
          Colors.black));

      // constant
      ret.add(_buildLine(phaseIndex + 0.1, dataPointsInitGuess[phaseIndex][1],
          phaseIndex + 0.9, dataPointsInitGuess[phaseIndex][1], Colors.black));

      // last
      ret.add(_buildLine(phaseIndex + 0.9, dataPointsInitGuess[phaseIndex][2],
          phaseIndex + 1, dataPointsInitGuess[phaseIndex][2], Colors.black));
    }
  }

  return ret;
}

LineChartBarData _buildLine(
    double x1, double y1, double x2, double y2, Color color) {
  return LineChartBarData(
    spots: [
      FlSpot(
        x1,
        y1,
      ),
      FlSpot(
        x2,
        y2,
      ),
    ],
    isCurved: true,
    color: color,
    dotData: const FlDotData(show: false),
    belowBarData: BarAreaData(show: false),
  );
}
