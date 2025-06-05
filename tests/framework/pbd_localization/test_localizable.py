import unittest
from unittest.mock import patch, MagicMock
from pbd_di import IDependencyBase
from pbd_localization import Localizable, NotDependencyBaseSubclassException, ILocalizer

class TestLocalizable(unittest.TestCase):

    @patch('pbd_di.IDependencyBase.get_dependency')
    def test_t_happy_path(self, mock_get_dependency):
        # Arrange
        mock_localizer = MagicMock()
        mock_localizer.t.return_value = 'Hello, World!'
        mock_get_dependency.return_value = mock_localizer
        class MockLocalizable(Localizable, IDependencyBase):
            pass
        localizable_instance = MockLocalizable()

        # Act
        result = localizable_instance.t('greeting')

        # Assert
        self.assertEqual(result, 'Hello, World!')
        mock_get_dependency.assert_called_once_with(ILocalizer)
        mock_localizer.t.assert_called_once_with('greeting', 'greeting')

    @patch('pbd_di.IDependencyBase.get_dependency')
    def test_t_with_default(self, mock_get_dependency):
        # Arrange
        mock_localizer = MagicMock()
        mock_localizer.t.return_value = 'Default Greeting'
        mock_get_dependency.return_value = mock_localizer
        class MockLocalizable(Localizable, IDependencyBase):
            pass
        localizable_instance = MockLocalizable()

        # Act
        result = localizable_instance.t('greeting', 'Default Greeting')

        # Assert
        self.assertEqual(result, 'Default Greeting')
        mock_get_dependency.assert_called_once_with(ILocalizer)
        mock_localizer.t.assert_called_once_with('greeting', 'Default Greeting')

    def test_not_dependency_base_subclass_exception(self):
        # Arrange & Act & Assert
        with self.assertRaises(NotDependencyBaseSubclassException):
            class InvalidLocalizable(Localizable):
                pass

    @patch('pbd_di.IDependencyBase.get_dependency')
    def test_t_localizer_exists(self, mock_get_dependency):
        # Arrange
        mock_localizer = MagicMock()
        mock_localizer.t.return_value = 'Hello, World!'
        class MockLocalizable(Localizable, IDependencyBase):
            def __init__(self):
                self._localizer = mock_localizer
        localizable_instance = MockLocalizable()

        # Act
        result = localizable_instance.t('greeting')

        # Assert
        self.assertEqual(result, 'Hello, World!')
        mock_get_dependency.assert_not_called()

    @patch('pbd_di.IDependencyBase.get_dependency')
    def test_t_localizer_returns_default_key(self, mock_get_dependency):
        # Arrange
        mock_localizer = MagicMock()
        mock_localizer.t.return_value = 'greeting'
        mock_get_dependency.return_value = mock_localizer
        class MockLocalizable(Localizable, IDependencyBase):
            pass
        localizable_instance = MockLocalizable()

        # Act
        result = localizable_instance.t('greeting')

        # Assert
        self.assertEqual(result, 'greeting')
        mock_get_dependency.assert_called_once_with(ILocalizer)
        mock_localizer.t.assert_called_once_with('greeting', 'greeting')