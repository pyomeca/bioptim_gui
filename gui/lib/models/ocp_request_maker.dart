import 'dart:convert';
import 'dart:io';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/decision_variables_type.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
import 'package:bioptim_gui/models/penalty.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';

///
/// [OCPRequestMaker] is a class that contains all the methods to make requests
/// for the different OCPs. (All request should be made through this class)
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

    return OCPAvailableValues(
      nodeValues,
      integrationRules,
      objectiveMin,
      objectiveMax,
      constraints,
      interpolationTypes,
      dynamics,
    );
  }

  void updateBioModel(List<File> files) async {
    if (files.length != 1) {
      throw Exception('Only one file can be selected');
    }
    final file = files[0];

    final url = Uri.parse('${APIConfig.url}/$prefix/model_path');
    final request = http.MultipartRequest('PUT', url);
    request.files.add(MultipartFile.fromBytes(
      'file',
      file.readAsBytesSync(),
      filename: file.path,
    ));

    request.send().then((response) async {
      if (response.statusCode != 200) {
        if (kDebugMode) {
          throw Exception(
              'Error while sending bioMod ${await response.stream.bytesToString()}');
        }
      }
    });

    if (kDebugMode) print("Updating bioMod");
  }

  Future<http.Response> updateField(String fieldName, dynamic newValue) async {
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

  Future<http.Response> updatePhaseField(
      int phaseIndex, String fieldName, dynamic newValue) async {
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

  Future<http.Response> updatePenaltyField(int phaseIndex, Type penaltyType,
      int penaltyIndex, String fieldName, dynamic value) async {
    final penaltyTypeString =
        penaltyType == Objective ? "objectives" : "constraints";
    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/$penaltyTypeString/$penaltyIndex/$fieldName');
    final body = json.encode({fieldName: value});

    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing $phaseInfoString $phaseIndex}\'s $penaltyTypeString $penaltyIndex} $fieldName to value $value');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex\'s $penaltyTypeString $penaltyIndex $fieldName changed to value $value');
    }

    return response;
  }

  Future<http.Response> updatePenaltyArgument(
      int phaseIndex,
      int penaltyIndex,
      String argumentName,
      String? newValue,
      String argumentType,
      Type penaltyType) async {
    final penaltyTypeString =
        penaltyType == Objective ? "objectives" : "constraints";

    final url = Uri.parse(
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/$penaltyTypeString/$penaltyIndex/arguments/$argumentName');
    final body = json.encode({
      "name": argumentName,
      "value": newValue,
      "type": argumentType,
    });

    final response =
        await http.put(url, body: body, headers: APIConfig.headers);

    if (response.statusCode != 200) {
      throw Exception(
          'Error while changing $phaseInfoString $phaseIndex\'s $penaltyTypeString $penaltyIndex $argumentName to value $newValue');
    }

    if (kDebugMode) {
      print(
          '$phaseInfoString $phaseIndex\'s $penaltyTypeString $penaltyIndex $argumentName changed to value $newValue');
    }
    return response;
  }

  Future<http.Response> updateDecisionVariableField(
      int phaseIndex,
      DecisionVariableType decisionVariableType,
      int variableIndex,
      String fieldName,
      dynamic newValue) async {
    final url =
        '${APIConfig.url}/$prefix/$phaseInfoString/$phaseIndex/${decisionVariableType.toPythonString()}/'
        '$variableIndex/$fieldName';

    final headers = {'Content-Type': 'application/json'};
    final body = json.encode({fieldName: newValue});
    final response =
        await http.put(Uri.parse(url), body: body, headers: headers);

    if (response.statusCode != 200) {
      throw Exception('Failed to update $fieldName to $newValue');
    }

    if (kDebugMode) print('$fieldName updated with value: $newValue');

    return response;
  }
}
