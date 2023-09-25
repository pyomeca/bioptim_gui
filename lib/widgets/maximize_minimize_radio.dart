import 'package:flutter/material.dart';

enum MinMax { maximize, minimize }

class MinMaxRadio extends StatefulWidget {
  const MinMaxRadio({super.key});

  @override
  State<MinMaxRadio> createState() => _MinMaxRadioState();
}

class _MinMaxRadioState extends State<MinMaxRadio> {
  MinMax? minOrMax = MinMax.minimize;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment:
          MainAxisAlignment.spaceBetween, // Adjust horizontal spacing
      children: <Widget>[
        Column(children: [
          Row(children: [
            Radio<MinMax>(
              value: MinMax.maximize,
              groupValue: minOrMax,
              onChanged: (MinMax? value) {
                setState(() {
                  minOrMax = value;
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
