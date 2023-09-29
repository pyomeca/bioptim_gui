import 'package:flutter/material.dart';

class CustomRadioButton<T> extends StatelessWidget {
  final T value;
  final List<T> items;
  final ValueChanged<T?>? customOnChanged;

  const CustomRadioButton({
    super.key,
    required this.value,
    required this.items,
    this.customOnChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        for (var item in items)
          Row(
            children: [
              Radio<T>(
                value: item,
                groupValue: value,
                onChanged: (newValue) {
                  if (newValue != null && customOnChanged != null) {
                    customOnChanged!(newValue);
                  }
                },
              ),
              Text(item.toString()),
            ],
          ),
      ],
    );
  }
}
