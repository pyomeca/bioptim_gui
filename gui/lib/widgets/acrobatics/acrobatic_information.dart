import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/acrobatics_request_maker.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/widgets/utils/positive_float_text_field.dart';
import 'package:bioptim_gui/widgets/utils/positive_integer_text_field.dart';
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:provider/provider.dart';

class AcrobaticInformation extends StatelessWidget {
  const AcrobaticInformation({
    super.key,
    required this.width,
  });

  final double width;

  @override
  Widget build(BuildContext context) {
    return Consumer<OCPData>(builder: (context, data, child) {
      final acrobaticsData = data as AcrobaticsData;
      return Column(
        children: [
          SizedBox(
            width: width,
            child: PositiveIntegerTextField(
              label: 'Number of somersaults *',
              value: acrobaticsData.nbSomersaults.toString(),
              onSubmitted: (newValue) async {
                if (newValue.isNotEmpty) {
                  final response = await AcrobaticsRequestMaker()
                      .updateField("nb_somersaults", newValue);

                  final updatedData =
                      AcrobaticsData.fromJson(json.decode(response.body));

                  acrobaticsData.updateData(updatedData);
                }
              },
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              SizedBox(
                width: width / 2 - 6,
                child: PositiveFloatTextField(
                  value: acrobaticsData.finalTime.toString(),
                  label: 'Final time *',
                  onSubmitted: (newValue) {
                    if (newValue.isNotEmpty) {
                      data.updateField("final_time", newValue);
                    }
                  },
                ),
              ),
              const SizedBox(width: 12),
              SizedBox(
                width: width / 2 - 6,
                child: PositiveFloatTextField(
                  value: acrobaticsData.finalTimeMargin.toString(),
                  label: 'Final time margin *',
                  onSubmitted: (newValue) {
                    if (newValue.isNotEmpty) {
                      data.updateField("final_time_margin", newValue);
                    }
                  },
                ),
              ),
            ],
          )
        ],
      );
    });
  }
}
