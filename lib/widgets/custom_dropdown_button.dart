import 'package:flutter/material.dart';

class CustomDropdownButton<T extends Object> extends StatelessWidget {
  const CustomDropdownButton({
    super.key,
    this.title,
    required this.value,
    required this.items,
    this.onSelected,
    this.isExpanded = false,
    this.color = Colors.black,
    this.focusColor = Colors.transparent,
    this.dropdownColor = Colors.white,
  });

  final T value;
  final Function(T)? onSelected;
  final String? title;
  final List<T> items;
  final bool isExpanded;
  final Color color;
  final Color focusColor;
  final Color dropdownColor;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<T>(
      decoration: InputDecoration(
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: color),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: color),
          ),
          label: title == null ? null : Text(title!),
          border: OutlineInputBorder(borderSide: BorderSide(color: color))),
      focusColor: focusColor,
      isExpanded: isExpanded,
      menuMaxHeight: MediaQuery.of(context).size.height * 1 / 2,
      value: value,
      items: items
          .map((e) => DropdownMenuItem(value: e, child: Text(e.toString())))
          .toList(),
      onChanged: onSelected == null ? null : (value) => onSelected!(value!),
      dropdownColor: dropdownColor,
    );
  }
}
