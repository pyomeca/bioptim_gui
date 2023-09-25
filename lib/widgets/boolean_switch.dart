import 'package:flutter/material.dart';

class BooleanSwitch extends StatefulWidget {
  final bool initialValue;
  final ValueChanged<bool> customOnChanged;
  final String leftTextOn;
  final String leftTextOff;
  final double width;

  const BooleanSwitch({
    Key? key,
    required this.customOnChanged,
    required this.initialValue,
    required this.leftTextOn,
    required this.leftTextOff,
    required this.width, // Add width as a parameter
  }) : super(key: key);

  @override
  BooleanSwitchState createState() => BooleanSwitchState();
}

class BooleanSwitchState extends State<BooleanSwitch> {
  late bool lightValue;
  late String leftText;

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
          Text(lightValue ? widget.leftTextOn : widget.leftTextOff),
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
