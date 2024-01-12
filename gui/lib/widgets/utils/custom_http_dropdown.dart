import 'package:bioptim_gui/models/api_config.dart';
import 'package:bioptim_gui/widgets/utils/custom_dropdown_button.dart';
import 'package:bioptim_gui/widgets/utils/extensions.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CustomHttpDropdown extends StatefulWidget {
  const CustomHttpDropdown({
    super.key,
    required this.title,
    required this.width,
    required this.defaultValue,
    this.getEndpoint,
    this.putEndpoint,
    this.requestKey,
    this.color = Colors.black,
    this.customStringFormatting = _defaultToString,
    this.customCallBack,
    this.customOnSelected,
    this.items,
  });

  final String title;
  final double width;
  final String defaultValue;
  final String? getEndpoint;
  final String? putEndpoint;
  // the key used in the request of the put method
  final String? requestKey;
  final Color color;
  final List<String>? items;

  final Function(String) customStringFormatting;
  static String _defaultToString(String s) => s.toString().toLowerCase();

  final Function(http.Response)? customCallBack;
  final Function(String)? customOnSelected;

  @override
  CustomHttpDropdownState createState() => CustomHttpDropdownState();
}

class CustomHttpDropdownState extends State<CustomHttpDropdown> {
  String _selectedValue = '';
  List<String> _availableValues = [];

  @override
  void initState() {
    super.initState();
    _selectedValue = widget.defaultValue;

    if (widget.items != null) {
      _availableValues = widget.items!;
    } else {
      _fetchAvailableValues();
    }
  }

  Future<void> _fetchAvailableValues() async {
    final url = Uri.parse('${APIConfig.url}${widget.getEndpoint}');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final List<dynamic> responseData = json.decode(response.body);
      final values = responseData
          .map((value) =>
              value.toString().replaceAll("_", " ").toLowerCase().capitalize())
          .toList();
      setState(() {
        _availableValues = values;
      });
    }
  }

  Future<void> _selectUpdate(String value) async {
    if (widget.customOnSelected != null) {
      final success = await widget.customOnSelected!(value);
      if (!success) {
        setState(() {
          _selectedValue = value;
        });
      }
    } else {
      setState(() {
        _selectedValue = value;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width,
      child: CustomDropdownButton<String>(
        value: _selectedValue,
        items: _availableValues,
        title: widget.title,
        onSelected: (value) =>
            {if (widget.customOnSelected != null) _selectUpdate(value)},
        color: widget.color,
      ),
    );
  }
}
