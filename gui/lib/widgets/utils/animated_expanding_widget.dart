import 'package:flutter/material.dart';

class AnimatedExpandingWidget extends StatefulWidget {
  const AnimatedExpandingWidget({
    super.key,
    required this.header,
    required this.child,
    this.expandingDuration = const Duration(milliseconds: 300),
    this.onTapHeader,
    this.initialExpandedState = false,
  });

  final Duration expandingDuration;
  final Widget header;
  final Function(bool newState)? onTapHeader;
  final Widget child;
  final bool initialExpandedState;

  @override
  State<AnimatedExpandingWidget> createState() =>
      _AnimatedExpandingWidgetState();
}

class _AnimatedExpandingWidgetState extends State<AnimatedExpandingWidget>
    with TickerProviderStateMixin {
  late bool _isExpanded = widget.initialExpandedState;

  late final AnimationController _expandingAnimationController =
      AnimationController(vsync: this, duration: widget.expandingDuration);
  late final Animation<double> _expandingAnimation = CurvedAnimation(
    parent: _expandingAnimationController,
    curve: Curves.fastOutSlowIn,
  );
  late final Tween<double> _expandingTween = Tween(begin: 0, end: 1);

  @override
  void initState() {
    super.initState();
    if (widget.initialExpandedState) {
      _expandingAnimationController.animateTo(1, duration: const Duration());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        InkWell(
          onTap: () {
            _isExpanded = !_isExpanded;
            _isExpanded
                ? _expandingAnimationController.forward()
                : _expandingAnimationController.reverse();

            if (widget.onTapHeader != null) widget.onTapHeader!(_isExpanded);
            setState(() {});
          },
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Flexible(child: widget.header),
              Padding(
                padding: const EdgeInsets.only(left: 12.0, right: 16.0),
                child: Icon(
                  _isExpanded ? Icons.expand_less : Icons.expand_more,
                  size: 30,
                  color: Colors.grey[700],
                ),
              )
            ],
          ),
        ),
        SizeTransition(
          sizeFactor: _expandingTween.animate(_expandingAnimation),
          child: widget.child,
        ),
      ],
    );
  }
}
