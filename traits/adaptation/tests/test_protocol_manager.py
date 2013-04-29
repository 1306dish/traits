""" Test the protocol manager. """


import unittest

from apptools.adaptation.adapter_registry import AdapterRegistry


class TestProtocolManager(unittest.TestCase):
    """ Test the protocol manager. """

    #### 'TestCase' protocol ##################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.protocol_manager = AdapterRegistry()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """

        return

    #### Tests ################################################################

    def test_no_adapter_required_with_abcs(self):

        from apptools.adaptation.tests.abc_examples import Foo, FooABC

        f = Foo()

        # Try to adapt it to its own concrete type.
        foo = self.protocol_manager.adapt(f, Foo)

        # The adapter  manager should simply return the same object.
        self.assert_(foo is f)

        # Try to adapt it to an ABC that is registered for its type.
        foo = self.protocol_manager.adapt(f, FooABC)

        # The adapter  manager should simply return the same object.
        self.assert_(foo is f)

        return

    def test_no_adapter_available_with_abcs(self):

        from apptools.adaptation.tests.abc_examples import (
            Bar, BarABC, Foo
        )

        f = Foo()

        # Try to adapt it to a concrete type.
        bar = self.protocol_manager.adapt(f, Bar)

        # There should be no way to adapt a Foo to a Bar.
        self.assertEqual(bar, None)

        # Try to adapt it to an ABC.
        bar = self.protocol_manager.adapt(f, BarABC)

        # There should be no way to adapt a Foo to a Bar.
        self.assertEqual(bar, None)

        return

    def test_adapter_available_on_type_of_adaptee_with_abcs(self):

        from apptools.adaptation.adapter_factory import AdapterFactory

        from apptools.adaptation.tests.abc_examples import (
            FooABCToBarABCAdapter,
            FooABC,
            BarABC,
            Foo,
            Bar
        )

        # FooABC->BarABC.
        self.protocol_manager.register_type_adapters(
            AdapterFactory(
                adapter_class = FooABCToBarABCAdapter,
                from_protocol = FooABC,
                to_protocol   = BarABC
            )
        )

        f = Foo()

        # Adapt it to an ABC.
        bar = self.protocol_manager.adapt(f, BarABC)
        self.assertIsNotNone(bar)
        self.assertIsInstance(bar, FooABCToBarABCAdapter)

        # We shouldn't be able to adapt it to a *concrete* 'Bar' though.
        bar = self.protocol_manager.adapt(f, Bar)
        self.assertIsNone(bar)

        return

    def test_adapter_chaining_with_abcs(self):

        from apptools.adaptation.adapter_factory import AdapterFactory

        from apptools.adaptation.tests.abc_examples import (
            FooABCToBarABCAdapter,
            BarABCToBazABCAdapter,
            FooABC,
            BarABC,
            BazABC,
            Foo
        )

        # FooABC->BarABC.
        self.protocol_manager.register_type_adapters(
            AdapterFactory(
                adapter_class = FooABCToBarABCAdapter,
                from_protocol = FooABC,
                to_protocol   = BarABC
            )
        )

        # BarABC->BazABC.
        self.protocol_manager.register_type_adapters(
            AdapterFactory(
                adapter_class = BarABCToBazABCAdapter,
                from_protocol = BarABC,
                to_protocol   = BazABC
            )
        )

        # Create a Foo.
        foo = Foo()

        # Adapt it to a BazABC via the chain.
        baz = self.protocol_manager.adapt(foo, BazABC)
        self.assertIsNotNone(baz)
        self.assertIsInstance(baz, BarABCToBazABCAdapter)
        self.assert_(baz.adaptee.adaptee is foo)
        
        return

    def test_adapter_chaining_with_interfaces(self):

        from apptools.adaptation.adapter_factory import AdapterFactory

        from apptools.adaptation.tests.interface_examples import (
            IFooToIBarAdapter,
            IBarToIBazAdapter,
            IFoo,
            IBar,
            IBaz,
            Foo
        )

        # IFoo->IBar.
        self.protocol_manager.register_type_adapters(
            AdapterFactory(
                adapter_class = IFooToIBarAdapter,
                from_protocol = IFoo,
                to_protocol   = IBar
            )
        )

        # IBar->IBaz.
        self.protocol_manager.register_type_adapters(
            AdapterFactory(
                adapter_class = IBarToIBazAdapter,
                from_protocol = IBar,
                to_protocol   = IBaz
            )
        )

        # Create a Foo.
        foo = Foo()

        # Adapt it to an IBaz via the chain.
        baz = self.protocol_manager.adapt(foo, IBaz)
        self.assertIsNotNone(baz)
        self.assertIsInstance(baz, IBarToIBazAdapter)
        self.assert_(baz.adaptee.adaptee is foo)
        
        return

#### EOF ######################################################################
