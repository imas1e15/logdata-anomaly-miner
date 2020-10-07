import unittest
import importlib
import yaml
import sys
from aminer.AnalysisChild import AnalysisContext
from aminer.analysis.AtomFilters import SubhandlerFilter
from aminer.analysis.NewMatchPathDetector import NewMatchPathDetector
from aminer.analysis.NewMatchPathValueDetector import NewMatchPathValueDetector
from aminer.analysis.NewMatchPathValueComboDetector import NewMatchPathValueComboDetector
from aminer.analysis.HistogramAnalysis import HistogramAnalysis, PathDependentHistogramAnalysis
from aminer.analysis.EnhancedNewMatchPathValueComboDetector import EnhancedNewMatchPathValueComboDetector
from aminer.analysis.MatchFilter import MatchFilter
from aminer.analysis.MatchValueAverageChangeDetector import MatchValueAverageChangeDetector
from aminer.analysis.MatchValueStreamWriter import MatchValueStreamWriter
from aminer.analysis.TimeCorrelationViolationDetector import TimeCorrelationViolationDetector
from aminer.analysis.TimestampCorrectionFilters import SimpleMonotonicTimestampAdjust
from aminer.analysis.TimestampsUnsortedDetector import TimestampsUnsortedDetector
from aminer.analysis.WhitelistViolationDetector import WhitelistViolationDetector
from aminer.events.StreamPrinterEventHandler import StreamPrinterEventHandler
from aminer.events.SyslogWriterEventHandler import SyslogWriterEventHandler
from aminer.events.DefaultMailNotificationEventHandler import DefaultMailNotificationEventHandler
from aminer.events.JsonConverterHandler import JsonConverterHandler
from aminer.input.SimpleByteStreamLineAtomizerFactory import SimpleByteStreamLineAtomizerFactory
from aminer.input.SimpleMultisourceAtomSync import SimpleMultisourceAtomSync
from aminer.parsing.FirstMatchModelElement import FirstMatchModelElement
from aminer.parsing.SequenceModelElement import SequenceModelElement
from aminer.parsing.VariableByteDataModelElement import VariableByteDataModelElement
from aminer.parsing.FixedDataModelElement import FixedDataModelElement
from aminer.parsing.DateTimeModelElement import DateTimeModelElement
from aminer.parsing.FixedWordlistDataModelElement import FixedWordlistDataModelElement
from aminer.parsing.DecimalIntegerValueModelElement import DecimalIntegerValueModelElement
from aminer.parsing.RepeatedElementDataModelElement import RepeatedElementDataModelElement
from aminer.parsing.OptionalMatchModelElement import OptionalMatchModelElement
from aminer.parsing.ElementValueBranchModelElement import ElementValueBranchModelElement


class YamlConfigTest(unittest.TestCase):
    sysp = sys.path

    def setUp(self):
        sys.path = sys.path[1:] + ['/usr/lib/logdata-anomaly-miner', '/etc/aminer/conf-enabled']

    def tearDown(self):
        sys.path = self.sysp

    def test1_load_generic_yaml_file(self):
        """Loads a yaml file into the variable aminer_config.yaml_data."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/template_config.yml')
        self.assertIsNotNone(aminer_config.yaml_data)

    def test2_load_notexistent_yaml_file(self):
        """Tries to load a nonexistent yaml file. A FileNotFoundError is expected."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(FileNotFoundError):
            aminer_config.load_yaml('unit/data/configfiles/doesnotexist.yml')

    def test3_load_invalid_yaml_file(self):
        """Tries to load a file with invalid yaml syntax. Expects an YAMLError."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(yaml.YAMLError):
            aminer_config.load_yaml('unit/data/configfiles/invalid_config.yml')

    def test4_load_yaml_file_with_invalid_schema(self):
        """Tries to load a yaml-file with an invalid schema. A ValueError is expected."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/invalid_schema.yml')

    def test5_analysis_pipeline_working_config(self):
        """This test builds a analysis_pipeline from a valid yaml-file."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/apache_inline_config.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        """ the following lines help to debug the context for defining the testcases
        from pprint import pprint
        pprint(vars(context))
        pprint(vars(context.atomizer_factory))
        pprint(vars(context.atomizer_factory.parsing_model))
        pprint(vars(context.atomizer_factory.atom_handler_list[0])) """
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.registered_components[1][0], TimestampsUnsortedDetector))
        self.assertTrue(isinstance(context.registered_components[2][0], NewMatchPathValueDetector))
        self.assertTrue(isinstance(context.registered_components[3][0], NewMatchPathValueComboDetector))
        self.assertTrue(isinstance(context.registered_components[4][0], HistogramAnalysis))
        self.assertTrue(isinstance(context.registered_components[5][0], PathDependentHistogramAnalysis))
        self.assertTrue(isinstance(context.registered_components[6][0], EnhancedNewMatchPathValueComboDetector))
        self.assertTrue(isinstance(context.registered_components[7][0], MatchFilter))
        self.assertTrue(isinstance(context.registered_components[8][0], MatchValueAverageChangeDetector))
        self.assertTrue(isinstance(context.registered_components[9][0], MatchValueStreamWriter))
        self.assertTrue(isinstance(context.registered_components[10][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.registered_components[11][0], TimeCorrelationViolationDetector))
        self.assertTrue(isinstance(context.registered_components[12][0], SimpleMonotonicTimestampAdjust))
        self.assertTrue(isinstance(context.registered_components[13][0], WhitelistViolationDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], StreamPrinterEventHandler))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[1], SyslogWriterEventHandler))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[2], DefaultMailNotificationEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[1], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[2], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[3], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[4], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[5], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[6], DateTimeModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[7], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[8], FixedWordlistDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[9], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[10], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[11], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[12], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[13], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[14], DecimalIntegerValueModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[15], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[16], DecimalIntegerValueModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[17], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[18], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[19], FixedDataModelElement))
        self.assertEqual(context.atomizer_factory.parsing_model.element_id, 'accesslog')

    def test6_analysis_fail_without_parser_start(self):
        """This test checks if the aminer fails without a start-tag for the first parser-model."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/missing_parserstart_config.yml')

    def test7_analysis_fail_with_double_parser_start(self):
        """This test checks if the aminer fails without a start-tag for the first parser-model."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/double_parserstart_config.yml')

    def test8_analysis_fail_with_unknown_parser_start(self):
        """This test checks if the config-schema-validator raises an error if an unknown parser is configured."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/unknown_parser_config.yml')

    def test9_analysis_pipeline_working_config_without_analysis_components(self):
        """This test checks if the config can be loaded without any analysis components."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/apache_inline_config_null_analysis_components.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.run_empty_components_tests(context)

        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/apache_inline_config_undefined_analysis_components.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.run_empty_components_tests(context)

    def test10_analysis_fail_with_unknown_analysis_component(self):
        """This test checks if the config-schema-validator raises an error if an unknown analysis component is configured."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/unknown_analysis_component.yml')

    def test11_analysis_fail_with_unknown_event_handler(self):
        """This test checks if the config-schema-validator raises an error if an unknown event handler is configured."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        with self.assertRaises(ValueError):
            aminer_config.load_yaml('unit/data/configfiles/unknown_event_handler.yml')

    def test12_analysis_pipeline_working_config_without_event_handler_components(self):
        """This test checks if the config can be loaded without any event handler components. This also tests if the
        StreamPrinterEventHandler was loaded by default."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/apache_inline_config_null_event_handlers.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.run_empty_components_tests(context)

        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/apache_inline_config_undefined_event_handlers.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.run_empty_components_tests(context)

    def test13_analysis_pipeline_working_with_json(self):
        """This test checks if JsonConverterHandler is working properly."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/json_config.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], JsonConverterHandler))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0].json_event_handlers[0], StreamPrinterEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], VariableByteDataModelElement))

    def test14_analysis_pipeline_working_with_learnMode(self):
        """This test checks if learnMode is working properly."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/learnMode_config.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.registered_components[1][0], NewMatchPathValueDetector))
        self.assertTrue(isinstance(context.registered_components[2][0], NewMatchPathValueComboDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], StreamPrinterEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], VariableByteDataModelElement))

        # learnMode: True should ignore all auto_include_flag arguments.
        for key in context.registered_components:
            self.assertTrue(context.registered_components[key][0].auto_include_flag)

        # learnMode: False should ignore all auto_include_flag arguments.
        aminer_config.yaml_data['LearnMode'] = False
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        for key in context.registered_components:
            self.assertFalse(context.registered_components[key][0].auto_include_flag)

        # unset learnMode: use auto_include_flag arguments
        del aminer_config.yaml_data['LearnMode']
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(context.registered_components[0][0].auto_include_flag)
        self.assertTrue(context.registered_components[1][0].auto_include_flag)
        self.assertFalse(context.registered_components[2][0].auto_include_flag)

        # unset learnMode and set auto_include_flag to default arguments: by default True should be used.
        for component in aminer_config.yaml_data['Analysis']:
            component['auto_include_flag'] = True
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(context.registered_components[0][0].auto_include_flag)
        self.assertTrue(context.registered_components[1][0].auto_include_flag)
        self.assertTrue(context.registered_components[2][0].auto_include_flag)

    def test15_analysis_pipeline_working_with_input_parameters(self):
        """This test checks if the SimpleMultisourceAtomSync and SimpleByteStreamLineAtomizerFactory are working properly."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/multiSource_config.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.registered_components[1][0], NewMatchPathValueDetector))
        self.assertTrue(isinstance(context.registered_components[2][0], NewMatchPathValueComboDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], StreamPrinterEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/model/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], VariableByteDataModelElement))

        # test with MultiSource: True. Expects a SimpleByteStreamLineAtomizerFactory with a SimpleMultisourceAtomSync.
        self.assertTrue(isinstance(context.atomizer_factory, SimpleByteStreamLineAtomizerFactory))
        self.assertTrue(isinstance(context.atomizer_factory.atom_handler_list[0], SimpleMultisourceAtomSync))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, [aminer_config.yaml_data['Input']['TimestampPath']])

        # test with MultiSource: False. Expects a SimpleByteStreamLineAtomizerFactory with a AtomFilters.SubhandlerFilter.
        aminer_config.yaml_data['Input']['MultiSource'] = False
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(isinstance(context.atomizer_factory, SimpleByteStreamLineAtomizerFactory))
        self.assertTrue(isinstance(context.atomizer_factory.atom_handler_list[0], SubhandlerFilter))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, [aminer_config.yaml_data['Input']['TimestampPath']])

    def test16_parsermodeltype_parameter_for_another_parsermodel_type(self):
        """This test checks if all ModelElements with child elements are working properly."""
        spec = importlib.util.spec_from_file_location('aminer_config', '/usr/lib/logdata-anomaly-miner/aminer/ymlconfig.py')
        aminer_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aminer_config)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')
        context = AnalysisContext(aminer_config)
        context.build_analysis_pipeline()
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.registered_components[1][0], NewMatchPathValueDetector))
        self.assertTrue(isinstance(context.registered_components[2][0], NewMatchPathValueComboDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], StreamPrinterEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/model/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, FirstMatchModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0].children[0], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0].children[1], RepeatedElementDataModelElement))
        self.assertTrue(isinstance(
            context.atomizer_factory.parsing_model.children[0].children[1].repeated_element, OptionalMatchModelElement))
        self.assertTrue(isinstance(
            context.atomizer_factory.parsing_model.children[0].children[1].repeated_element.optional_element, FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[1], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[2], ElementValueBranchModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[2].value_model, FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[2].branch_model_dict['host'], FixedDataModelElement))

        # change OptionalModelElement to unknown_model
        aminer_config.yaml_data['Parser'][1]['args'] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

        # change RepeatedElementDataModelElement to unknown_model
        aminer_config.yaml_data['Parser'][2]['args'][0] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

        # change SequenceModelElement to unknown_model
        aminer_config.yaml_data['Parser'][3]['args'][1] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

        # change ElementValueBranchModelElement to unknown_model
        aminer_config.yaml_data['Parser'][4]['args'][0] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

        aminer_config.yaml_data['Parser'][4]['branch_model_dict'][0]['model'] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

        # change FirstMatchModelElement to unknown_model
        aminer_config.yaml_data['Parser'][5]['args'][1] = b'unknown_model'
        context = AnalysisContext(aminer_config)
        self.assertRaises(ValueError, context.build_analysis_pipeline)
        aminer_config.load_yaml('unit/data/configfiles/parser_child_elements_config.yml')

    def test17_demo_config_working_as_expected(self):
        """This test checks if the yaml demo config loads properly."""
        self.assertTrue(True)
        raise Exception("not implemented yet..")

    def test18_demo_yaml_config_equals_python_config(self):
        """This test checks if the yaml demo config is the same as the python version."""
        self.assertTrue(True)
        raise Exception("not implemented yet..")

    def run_empty_components_tests(self, context):
        """ the following lines help to debug the context for defining the testcases
        from pprint import pprint
        pprint(vars(context))
        pprint(vars(context.atomizer_factory))
        pprint(vars(context.atomizer_factory.parsing_model))
        pprint(vars(context.atomizer_factory.atom_handler_list[0])) """
        self.assertTrue(isinstance(context.registered_components[0][0], NewMatchPathDetector))
        self.assertTrue(isinstance(context.atomizer_factory.event_handler_list[0], StreamPrinterEventHandler))
        self.assertEqual(context.atomizer_factory.default_timestamp_paths, ['/accesslog/time'])
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model, SequenceModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[0], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[1], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[2], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[3], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[4], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[5], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[6], DateTimeModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[7], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[8], FixedWordlistDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[9], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[10], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[11], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[12], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[13], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[14], DecimalIntegerValueModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[15], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[16], DecimalIntegerValueModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[17], FixedDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[18], VariableByteDataModelElement))
        self.assertTrue(isinstance(context.atomizer_factory.parsing_model.children[19], FixedDataModelElement))
        self.assertEqual(context.atomizer_factory.parsing_model.element_id, 'accesslog')


if __name__ == "__main__":
    unittest.main()
