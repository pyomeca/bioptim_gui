import 'package:bioptim_gui/models/generic_ocp_data.dart';
import 'package:bioptim_gui/models/generic_ocp_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/screens/generate_code_page/generic/generate_phases.dart';
import 'package:bioptim_gui/widgets/generic_ocp/number_of_phases_chooser.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class GenericMenu extends StatefulWidget {
  const GenericMenu({super.key, this.columnWidth = 400.0});

  final double columnWidth;

  @override
  State<GenericMenu> createState() => _GenericMenuState();
}

class _GenericMenuState extends State<GenericMenu> {
  final _verticalScroll = ScrollController();

  GenericOcpData? _data;

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
      return ChangeNotifierProvider<OCPData>(
        create: (context) => _data!,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            _HeaderBuilder(width: widget.columnWidth),
            const SizedBox(height: 12),
            const Divider(),
            const SizedBox(height: 12),
            _PhaseBuilder(
              width: widget.columnWidth,
            ),
          ],
        ),
      );
    }
  }
}

class _HeaderBuilder extends StatelessWidget {
  const _HeaderBuilder({
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        width: width,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 12),
                NumberOfPhasesChooser(width: width),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _PhaseBuilder extends StatefulWidget {
  const _PhaseBuilder({
    required this.width,
  });

  final double width;

  @override
  State<_PhaseBuilder> createState() => _PhaseBuilderState();
}

class _PhaseBuilderState extends State<_PhaseBuilder> {
  final _horizontalScroll = ScrollController();

  @override
  void dispose() {
    _horizontalScroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RawScrollbar(
      controller: _horizontalScroll,
      thumbVisibility: true,
      thumbColor: Theme.of(context).colorScheme.secondary,
      thickness: 8,
      radius: const Radius.circular(25),
      child: SingleChildScrollView(
        controller: _horizontalScroll,
        scrollDirection: Axis.horizontal,
        child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              PhaseGenerationMenu(
                width: widget.width,
              ),
            ]),
      ),
    );
  }
}
