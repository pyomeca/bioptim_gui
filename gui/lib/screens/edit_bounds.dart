import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/acrobatics_request_maker.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/edit_bounds/bound_chart.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class EditBounds extends StatefulWidget {
  const EditBounds({super.key, required this.endpointPrefix});

  final String endpointPrefix;

  @override
  State<EditBounds> createState() => _EditBoundsState();
}

class _EditBoundsState extends State<EditBounds> {
  AcrobaticsData? _data;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final data = await AcrobaticsRequestMaker().fetchData();
    setState(() {
      _data = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_data == null) {
      return const CircularProgressIndicator();
    } else {
      return ChangeNotifierProvider<OCPData>(
        create: (context) => _data!,
        child: SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: Column(
            children: [
              for (int dofIndex = 0;
                  dofIndex < _data!.phasesInfo[0].stateVariables[0].dimension;
                  dofIndex++)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: 100.0,
                      child: Text(
                        _data!.dofNames[dofIndex],
                        overflow: TextOverflow.clip,
                      ),
                    ),
                    for (int variableIndex = 0;
                        variableIndex <
                            (_data!.phasesInfo[0].stateVariables.length);
                        variableIndex++)
                      BoundChart(
                        key: Key('BoundChart_${dofIndex}_state_$variableIndex'),
                        decisionVariableType: DecisionVariableType.state,
                        variableIndex: variableIndex,
                        dofIndex: dofIndex,
                      ),
                  ],
                ),
            ],
          ),
        ),
      );
    }
  }
}
