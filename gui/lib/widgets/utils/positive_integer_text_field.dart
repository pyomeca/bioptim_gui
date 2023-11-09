import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PositiveIntegerTextField extends StatefulWidget {
  const PositiveIntegerTextField({
    super.key,
    this.label,
    required this.value,
    this.onSubmitted,
    this.onChanged,
    this.enabled = true,
    this.allowZero = false,
    this.color = Colors.black,
  });

  final String? label;
  final String value;
  final Function(int value)? onChanged;
  final bool enabled;
  final bool allowZero;
  final Color color;
  final ValueChanged<String>? onSubmitted;

  @override
  State<PositiveIntegerTextField> createState() =>
      _PositiveIntegerTextFieldState();
}

class _PositiveIntegerTextFieldState extends State<PositiveIntegerTextField> {
  Color color = Colors.black;

  @override
  void initState() {
    // if label ends with *, it is mandatory, and the color is red
    if (widget.label != null && widget.label!.endsWith('*')) {
      color = Colors.red;
    } else {
      color = widget.color;
    }
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      child: TextField(
        controller: TextEditingController(text: widget.value),
        decoration: InputDecoration(
            enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: color),
            ),
            focusedBorder: OutlineInputBorder(
              borderSide: BorderSide(color: color),
            ),
            labelText: widget.label,
            border: const OutlineInputBorder()),
        inputFormatters: [FilteringTextInputFormatter.digitsOnly],
        onSubmitted: widget.onSubmitted,
        enabled: widget.enabled,
      ),
    );
  }
}
