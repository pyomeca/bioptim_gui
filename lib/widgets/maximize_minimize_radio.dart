import 'package:flutter/material.dart';

enum MinMax {
  maximize,
  minimize,
  ;

  @override
  String toString() {
    switch (this) {
      case MinMax.maximize:
        return 'Maximize';
      case MinMax.minimize:
        return 'Minimize';
    }
  }

  String toPythonString() {
    switch (this) {
      case MinMax.maximize:
        return '-'; // will be used to negate the weight for maximizing
      case MinMax.minimize:
        return '';
    }
  }
}

class MinMaxRadio extends StatefulWidget {
  final MinMax value; // Added the 'value' property
  final ValueChanged<MinMax?>
      customOnChanged; // Added the 'customOnChanged' property

  const MinMaxRadio({
    Key? key,
    required this.value, // Specify 'value' in the constructor
    required this.customOnChanged, // Specify 'customOnChanged' in the constructor
  }) : super(key: key);

  @override
  State<MinMaxRadio> createState() => _MinMaxRadioState();
}

class _MinMaxRadioState extends State<MinMaxRadio> {
  late MinMax? minOrMax;

  @override
  void initState() {
    super.initState();
    minOrMax = widget.value; // Initialize 'minOrMax' with the provided 'value'
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        Column(children: [
          Row(children: [
            Radio<MinMax>(
              value: MinMax.maximize,
              groupValue: minOrMax,
              onChanged: (MinMax? value) {
                setState(() {
                  minOrMax = value;
                  widget.customOnChanged(
                      value); // Call the custom onChanged callback
                });
              },
            ),
            const Text('Maximize'),
          ]),
          Row(children: [
            Radio<MinMax>(
              value: MinMax.minimize,
              groupValue: minOrMax,
              onChanged: (MinMax? value) {
                setState(() {
                  minOrMax = value;
                  widget.customOnChanged(
                      value); // Call the custom onChanged callback
                });
              },
            ),
            const Text('Minimize'),
          ]),
        ]),
      ],
    );
  }
}
