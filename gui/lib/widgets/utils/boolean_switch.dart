import 'package:flutter/material.dart';

class BooleanSwitch extends StatefulWidget {
  final bool initialValue;
  final ValueChanged<bool> customOnChanged;
  final String leftText;
  final double width;

  const BooleanSwitch({
    Key? key,
    required this.customOnChanged,
    required this.initialValue,
    required this.leftText,
    required this.width, // Add width as a parameter
  }) : super(key: key);

  @override
  BooleanSwitchState createState() => BooleanSwitchState();
}

class BooleanSwitchState extends State<BooleanSwitch> {
  late bool lightValue;

  @override
  void initState() {
    super.initState();
    lightValue = widget.initialValue;
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.width, // Set the width based on the widget's parameter
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(widget.leftText),
          Switch(
            value: lightValue,
            onChanged: (bool value) {
              setState(() {
                lightValue = value;
              });
              widget.customOnChanged(value);
            },
            thumbIcon: MaterialStateProperty.resolveWith<Icon?>(
              (Set<MaterialState> states) {
                if (states.contains(MaterialState.selected)) {
                  return const Icon(Icons.check);
                }
                return const Icon(Icons.close);
              },
            ),
          ),
        ],
      ),
    );
  }
}
