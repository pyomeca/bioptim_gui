import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class AcrobaticsRequestMaker extends OCPRequestMaker<AcrobaticsData> {
  AcrobaticsRequestMaker()
      : super(prefix: 'acrobatics', phaseInfoString: 'phases_info');

  Future<AcrobaticsData> fetchData() async {
    final url = Uri.parse('${APIConfig.url}/$prefix/');
    final response = await http.get(url);

    if (response.statusCode != 200) throw Exception("Fetch error");
    if (kDebugMode) print("Data fetch success.");

    final data = json.decode(response.body);

    var acrobaticsData = AcrobaticsData.fromJson(data);
    AcrobaticsAvailableValues availableValues = await getAvailableValues();
    acrobaticsData.availablesValue = availableValues;

    return acrobaticsData;
  }

  @override
  Future<AcrobaticsAvailableValues> getAvailableValues() async {
    final url = Uri.parse('${APIConfig.url}/$prefix/available_values');
    final response = await http.get(url);
    final jsonResponse = json.decode(response.body);

    List<String> nodeValues = List<String>.from(jsonResponse["nodes"]);
    List<String> integrationRules =
        List<String>.from(jsonResponse["integration_rules"]);
    List<String> objectiveMin =
        List<String>.from(jsonResponse["objectives"]["minimize"]);
    List<String> objectiveMax =
        List<String>.from(jsonResponse["objectives"]["maximize"]);
    List<String> constraints = List<String>.from(jsonResponse["constraints"]);
    List<String> interpolationTypes =
        List<String>.from(jsonResponse["interpolation_types"]);
    List<String> dynamics = List<String>.from(jsonResponse["dynamics"]);
    List<String> position = List<String>.from(jsonResponse["positions"]);
    List<String> sportType = List<String>.from(jsonResponse["sport_types"]);
    List<String> preferredTwistSide =
        List<String>.from(jsonResponse["preferred_twist_sides"]);

    return AcrobaticsAvailableValues(
      nodeValues,
      integrationRules,
      objectiveMin,
      objectiveMax,
      constraints,
      interpolationTypes,
      dynamics,
      position,
      sportType,
      preferredTwistSide,
    );
  }

  Future<http.Response> updateHalfTwists(int index, int value) async {
    final url = Uri.parse('${APIConfig.url}/$prefix/nb_half_twists/$index');
    final body = json.encode({"nb_half_twists": value});
    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception('Failed to update nb_half_twists $index');
    }

    if (kDebugMode) print('nb_half_twists $index updated with value: $value');
    return response;
  }
}
