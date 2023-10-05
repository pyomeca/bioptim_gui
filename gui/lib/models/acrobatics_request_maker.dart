import 'dart:convert';

import 'package:bioptim_gui/models/acrobatics_data.dart';
import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class AcrobaticsRequestMaker extends OCPRequestMaker<AcrobaticsData> {
  AcrobaticsRequestMaker()
      : super(prefix: 'acrobatics', phaseInfoString: 'somersaults_info');

  Future<AcrobaticsData> fetchData() async {
    final url = Uri.parse('${APIConfig.url}/$prefix');
    final response = await http.get(url);

    if (response.statusCode != 200) throw Exception("Fetch error");

    if (kDebugMode) print("Data fetch success.");

    final data = json.decode(response.body);
    return AcrobaticsData.fromJson(data);
  }
}
