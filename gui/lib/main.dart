import 'package:bioptim_gui/models/python_interface.dart';
import 'package:bioptim_gui/screens/generate_code_page/generate_code_page.dart';
import 'package:bioptim_gui/screens/generate_model.dart';
import 'package:bioptim_gui/screens/load_existing_page.dart';
import 'package:flutter/material.dart';
import 'package:window_manager/window_manager.dart';

void main() async {
  //needed to ensure binding was initialized
  WidgetsFlutterBinding.ensureInitialized();

  await WindowManager.instance.ensureInitialized();
  await windowManager.waitUntilReadyToShow();
  await windowManager.setTitle('Bioptim GUI code generator');

  PythonInterface.instance.initialize(environment: 'bioptim_gui');

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
      home: const SideMenuNavigation(),
    );
  }
}

class SideMenuNavigation extends StatefulWidget {
  const SideMenuNavigation({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _SideMenuNavigationState createState() => _SideMenuNavigationState();
}

class _SideMenuNavigationState extends State<SideMenuNavigation> {
  int _selectedMenuItemIndex = 0;

  final List<Widget> _pages = [
    const GenerateCode(),
    const GenerateModel(),
    const LoadExisting(),
  ];

  final List<String> _pageTitles = [
    'Bioptim Generate Code',
    'Generate Model',
    'Load existing solution',
  ];

  final List<String> _drawerItemTitles = [
    'Generate Code',
    'Generate Model',
    'Load existing solution',
  ];

  void _onMenuItemSelected(int index) {
    setState(() {
      _selectedMenuItemIndex = index;
      Navigator.of(context).pop(); // Close the side menu
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(_pageTitles[
            _selectedMenuItemIndex]), // Update app bar title dynamically
        leading: Builder(
          builder: (context) {
            return IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {
                Scaffold.of(context).openDrawer();
              },
            );
          },
        ),
      ),
      drawer: Drawer(
        child: ListView.builder(
          itemCount: _pages.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(
                  _drawerItemTitles[index]), // Use custom drawer item titles
              onTap: () => _onMenuItemSelected(index),
              selected: index == _selectedMenuItemIndex,
            );
          },
        ),
      ),
      body: _pages[_selectedMenuItemIndex],
    );
  }
}
