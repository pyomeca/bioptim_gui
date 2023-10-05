import 'dart:convert';

import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/models/generic_ocp_data.dart';
import 'package:bioptim_gui/models/ocp_request_maker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class GenericOCPRequestMaker extends OCPRequestMaker<GenericOcpData> {
  GenericOCPRequestMaker()
      : super(prefix: 'generic_ocp', phaseInfoString: 'phases_info');

  Future<GenericOcpData> fetchData() async {
    final url = Uri.parse('${APIConfig.url}/$prefix');
    final response = await http.get(url);

    if (response.statusCode != 200) throw Exception("Fetch error");

    if (kDebugMode) print("Data fetch success.");

    final data = json.decode(response.body);
    return GenericOcpData.fromJson(data);
  }
}
