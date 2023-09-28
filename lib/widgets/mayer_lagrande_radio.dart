import 'package:flutter/material.dart';

enum MayerLagrange {
  mayer,
  lagrange,
  ;

  @override
  String toString() {
    switch (this) {
      case mayer:
        return '\u2133'; // German mark M
      case lagrange:
        return '\u2112'; // Laplace L
    }
  }
}

class MayerLagrangeRadio extends StatefulWidget {
  final MayerLagrange value;
  final ValueChanged<MayerLagrange?> customOnChanged;

  const MayerLagrangeRadio({
    Key? key,
    required this.value,
    required this.customOnChanged,
  }) : super(key: key);

  @override
  State<MayerLagrangeRadio> createState() => _MinMaxRadioState();
}

class _MinMaxRadioState extends State<MayerLagrangeRadio> {
  late MayerLagrange? mayerOrLagrange;

  @override
  void initState() {
    super.initState();
    mayerOrLagrange = widget.value;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        for (var type in MayerLagrange.values)
          Row(children: [
            Radio<MayerLagrange>(
              value: type,
              groupValue: mayerOrLagrange,
              onChanged: (MayerLagrange? value) {
                setState(() {
                  mayerOrLagrange = value;
                  widget.customOnChanged(value);
                });
              },
            ),
            Text(type.toString()),
          ]),
      ],
    );
  }
}
