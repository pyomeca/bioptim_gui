import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/ocp_data.dart';
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
    OCPAvailableValues availableValues = await getAvailableValues();
    acrobaticsData.availablesValue = availableValues;

    return acrobaticsData;
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
