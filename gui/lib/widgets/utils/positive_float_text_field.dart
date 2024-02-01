import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class PositiveFloatTextField extends StatefulWidget {
  const PositiveFloatTextField({
    super.key,
    required this.label,
    required this.value,
    this.enabled = true,
    this.allowZero = false,
    this.color = Colors.black,
    this.onSubmitted,
  });

  final String label;
  final String value;
  final bool enabled;
  final bool allowZero;
  final Color color;
  final ValueChanged<String>? onSubmitted;

  @override
  State<PositiveFloatTextField> createState() => _PositiveFloatTextFieldState();
}

class _PositiveFloatTextFieldState extends State<PositiveFloatTextField> {
  Color color = Colors.black;

  @override
  void initState() {
    // if label ends with *, it is mandatory, and the color is red
    if (widget.label.endsWith('*')) {
      color = Colors.red;
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
        inputFormatters: [
          FilteringTextInputFormatter.allow(RegExp(r'[0-9\.]'))
        ],
        onSubmitted: widget.onSubmitted,
      ),
    );
  }
}
