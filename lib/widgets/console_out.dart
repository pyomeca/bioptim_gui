import 'package:flutter/material.dart';

class ConsoleOut extends StatelessWidget {
  const ConsoleOut({
    super.key,
    required this.output,
    this.textColor = Colors.white,
  });

  final Stream<String> output;
  final Color textColor;

  @override
  Widget build(BuildContext context) {
    final scrollController = ScrollController();

    return StreamBuilder(
      stream: output,
      builder: (context, snapshot) {
        if (!snapshot.hasData) return Container();
        return Container(
          decoration: BoxDecoration(
              border: Border.all(color: Colors.grey, width: 5),
              color: Colors.black),
          height: 700,
          width: MediaQuery.of(context).size.width * 3 / 4,
          child: RawScrollbar(
            thumbColor: Colors.white,
            thumbVisibility: true,
            controller: scrollController,
            radius: const Radius.circular(25),
            thickness: 8,
            child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12.0),
                child: SingleChildScrollView(
                  controller: scrollController,
                  child: Theme(
                    data: Theme.of(context).copyWith(
                        textSelectionTheme: const TextSelectionThemeData(
                            selectionColor: Colors.grey)),
                    child: SelectableText(
                      snapshot.data!,
                      cursorColor: Colors.red,
                      style: TextStyle(color: textColor),
                    ),
                  ),
                )),
          ),
        );
      },
    );
  }
}
