import 'package:flutter/material.dart';

class CustomDropdownButton<T extends Object> extends StatelessWidget {
  const CustomDropdownButton({
    super.key,
    this.title,
    required this.value,
    required this.items,
    this.onSelected,
    this.isExpanded = false,
    this.color,
  });

  final T value;
  final Function(T)? onSelected;
  final String? title;
  final List<T> items;
  final bool isExpanded;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<T>(
      decoration: InputDecoration(
          label: title == null ? null : Text(title!),
          border: const OutlineInputBorder(
              borderSide: BorderSide(color: Colors.black))),
      focusColor: Colors.transparent,
      isExpanded: isExpanded,
      menuMaxHeight: MediaQuery.of(context).size.height * 1 / 2,
      value: value,
      items: items
          .map((e) => DropdownMenuItem(value: e, child: Text(e.toString())))
          .toList(),
      onChanged: onSelected == null ? null : (value) => onSelected!(value!),
      dropdownColor: Colors.white,
    );
  }
}
