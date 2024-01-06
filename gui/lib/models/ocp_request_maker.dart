import 'dart:convert';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

///
/// [OCPRequestMaker] is a class that contains all the methods to make requests
/// for the different OCPs.
/// As the OCPs endpoints are all very similar, this class is used as a parent
/// class to reduce code duplication.
/// example: the only thing that differs between the "generic OCP" and the
/// "acrobatics OCP" is the endpoint beginning "generic_ocp/phases_info" or
/// "acrobatics/phases_info".
class OCPRequestMaker<T extends OCPData> {
  OCPRequestMaker({required this.prefix, required this.phaseInfoString});

  final String prefix;
  final String phaseInfoString;

  Future<OCPAvailableValues> getAvailableValues() async {
    final url = Uri.parse('${APIConfig.url}/penalties/available_values');
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

    return OCPAvailableValues(
      nodeValues,
      integrationRules,
      objectiveMin,
      objectiveMax,
      constraints,
    );
  }

  Future<http.Response> updateField(String fieldName, String newValue) async {
    final url = Uri.parse('${APIConfig.url}/$prefix/$fieldName');
    final body = json.encode({fieldName: newValue});
    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception('Failed to update $fieldName');
    }

    if (kDebugMode) print('$fieldName updated with value: $newValue');
    return response;
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

  Future<http.Response> updatePhaseField(
      int phaseIndex, String fieldName, String newValue) async {
    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/$fieldName');
    final body = json.encode({fieldName: newValue});
    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception(
          'Failed to update $phaseInfoString $phaseIndex\'s $fieldName');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex, $fieldName updated with value: $newValue');
    }
    return response;
  }

  Future<http.Response> updateMaximizeMinimize(
      int phaseIndex, int objectiveIndex, String value) async {
    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/objectives/$objectiveIndex/weight/$value');

    final response = await http.put(url);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing $phaseInfoString $phaseIndex\'s objective $objectiveIndex to value $value');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex\'s objective $objectiveIndex changed to value $value');
    }

    return response;
  }

  Future<http.Response> updatePenaltyField(int phaseIndex, String penaltyType,
      int penaltyIndex, String fieldName, dynamic value) async {
    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/$penaltyType/$penaltyIndex/$fieldName');
    final body = json.encode({fieldName: value});

    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing $phaseInfoString $phaseIndex}\'s $penaltyType $penaltyIndex} $fieldName to value $value');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex\'s $penaltyType $penaltyIndex $fieldName changed to value $value');
    }

    return response;
  }

  Future<http.Response> updatePenaltyArgument(
      int phaseIndex,
      int penaltyIndex,
      String argumentName,
      String? newValue,
      String argumentType,
      String penaltyType) async {
    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/$penaltyType/$penaltyIndex/arguments/$argumentName');
    final body = json.encode({
      "name": argumentName,
      "value": newValue,
      "type": argumentType,
    });

    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing $phaseInfoString $phaseIndex\'s $penaltyType $penaltyIndex $argumentName to value $newValue');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex\'s $penaltyType $penaltyIndex $argumentName changed to value $newValue');
    }
    return response;
  }
}
