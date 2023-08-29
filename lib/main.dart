import 'package:bioptim_gui/screens/main_page.dart';
import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

void main() async {
  //needed to ensure binding was initialized
  WidgetsFlutterBinding.ensureInitialized();

  await WindowManager.instance.ensureInitialized();
  await windowManager.waitUntilReadyToShow();
  await windowManager.setTitle('Bioptim GUI code generator');

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.amber),
        useMaterial3: true,
      ),
      home: const MainPage(),
    );
  }
}
