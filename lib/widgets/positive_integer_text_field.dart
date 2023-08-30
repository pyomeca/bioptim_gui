import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PositiveIntegerTextField extends StatefulWidget {
  const PositiveIntegerTextField({
    super.key,
    this.label,
    required this.controller,
    this.onChanged,
    this.enabled = true,
    this.allowZero = false,
  });

  final String? label;
  final TextEditingController controller;
  final Function(int value)? onChanged;
  final bool enabled;
  final bool allowZero;

  @override
  State<PositiveIntegerTextField> createState() =>
      _PositiveIntegerTextFieldState();
}

class _PositiveIntegerTextFieldState extends State<PositiveIntegerTextField> {
  @override
  Widget build(BuildContext context) {
    return Focus(
      onFocusChange: (hasFocus) {
        if (!hasFocus) {
          int? value = int.tryParse(widget.controller.text);
          if (value == null) {
            value = 1;
            widget.controller.text = '1';
          }
          if (widget.onChanged != null) widget.onChanged!(value);
        }
      },
      child: TextField(
        controller: widget.controller,
        decoration: InputDecoration(
            labelText: widget.label, border: const OutlineInputBorder()),
        inputFormatters: [FilteringTextInputFormatter.digitsOnly],
        enabled: widget.enabled,
      ),
    );
  }
}
