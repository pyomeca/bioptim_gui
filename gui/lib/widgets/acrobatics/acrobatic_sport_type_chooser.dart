import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/custom_http_dropdown.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AcrobaticSportTypeChooser extends StatelessWidget {
  const AcrobaticSportTypeChooser({
    super.key,
    required this.width,
    this.defaultValue = "Trampoline",
  });

  final double width;
  final String defaultValue;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      return CustomHttpDropdown(
        title: "Sport type",
        width: width,
        defaultValue: defaultValue,
        items: ((data as AcrobaticsData).availablesValue!
                as AcrobaticsAvailableValues)
            .sportTypes,
        putEndpoint: "/acrobatics/sport_type",
        requestKey: "sport_type",
        customOnSelected: (value) async {
          data.updateField("sport_type", value.toLowerCase());
          return true;
        },
      );
    });
  }
}
