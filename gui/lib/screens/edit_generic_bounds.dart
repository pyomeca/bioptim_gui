import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/generic_ocp_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/edit_bounds/variable_chart_expander.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class EditGenericBounds extends StatefulWidget {
  const EditGenericBounds({
    super.key,
    this.columnWidth = 1080.0,
  });

  final double columnWidth;

  @override
  State<EditGenericBounds> createState() => _EditGenericBoundsState();
}

class _EditGenericBoundsState extends State<EditGenericBounds> {
  OCPData? _data;
  final _verticalScroll = ScrollController();

  @override
  void dispose() {
    _verticalScroll.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final data = await GenericOCPRequestMaker().fetchData();
    setState(() {
      _data = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_data == null) {
      return const CircularProgressIndicator();
    } else {
      return Scaffold(
        body: RawScrollbar(
          controller: _verticalScroll,
          thumbVisibility: true,
          thumbColor: Theme.of(context).colorScheme.secondary,
          thickness: 8,
          radius: const Radius.circular(25),
          child: SingleChildScrollView(
            controller: _verticalScroll,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const SizedBox(height: 12),
                // const OptimalControlProgramTypeChooser(
                //   width: 400.0,
                // ), // TODO implement chooser to edit generic ocp bounds
                const SizedBox(height: 12),
                Center(
                  child: SizedBox(
                    width: widget.columnWidth,
                    child: ChangeNotifierProvider<OCPData>(
                      create: (context) => _data!,
                      child: const Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          VariableChart(
                            decisionVariableType: DecisionVariableType.state,
                          ),
                          VariableChart(
                            decisionVariableType: DecisionVariableType.control,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }
  }
}
