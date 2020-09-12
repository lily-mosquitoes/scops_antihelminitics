import string, random
from django.test import TestCase
from django.db import IntegrityError
from drug_database.models import ActiveComponent, Company, Product, DrugUse, SheepDrugType, SheepPathogen, SheepDrug


def get_random_string(length):

    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class ActiveComponentTestCase(TestCase):

    def setUp(self):

        self.active_component = get_random_string(8)

    def test_active_component_class_works(self):

        try:
            ActiveComponent.objects.create(active_component=self.active_component)
        except IntegrityError as e:
            self.fail(e)

    def test_active_component_is_required(self):

        with self.assertRaises(IntegrityError):
            ActiveComponent.objects.create(active_component=None)

    def test_active_component_is_unique(self):

        ActiveComponent.objects.create(active_component=self.active_component)

        with self.assertRaises(IntegrityError):
            ActiveComponent.objects.create(active_component=self.active_component)


class CompanyTestCase(TestCase):

    def setUp(self):

        self.company = get_random_string(8)

    def test_company_class_works(self):

        try:
            Company.objects.create(company=self.company)
        except IntegrityError as e:
            self.fail(e)

    def test_company_is_required(self):

        with self.assertRaises(IntegrityError):
            Company.objects.create(company=None)

    def test_company_is_unique(self):

        Company.objects.create(company=self.company)

        with self.assertRaises(IntegrityError):
            Company.objects.create(company=self.company)


class ProductTestCase(TestCase):

    def setUp(self):

        self.product_name = get_random_string(8)

        company = get_random_string(8)
        Company.objects.create(company=company)
        self.company = Company.objects.get(company=company)

    def make_active_component_list(self, length):

        active_component_list = list()
        for _ in range(length):
            active_component = get_random_string(8)
            ActiveComponent.objects.create(active_component=active_component)
            a = ActiveComponent.objects.get(active_component=active_component)
            active_component_list.append(a)

        return active_component_list

    def test_product_class_works(self):

        try:
            # active_component can be null on database
            Product.objects.create(product_name=self.product_name, company=self.company)
        except IntegrityError as e:
            self.fail(e)

    def test_product_name_is_required(self):

        with self.assertRaises(IntegrityError):
            # active_component can be null on database
            Product.objects.create(product_name=None, company=self.company)

    def test_company_is_required(self):

        with self.assertRaises(IntegrityError):
            # active_component can be null on database
            Product.objects.create(product_name=self.product_name, company=None)

    # ManyToManyField 'active_component' cannot be enforced by database

    def test_product_name_is_unique(self):

        # active_component can be null on database
        Product.objects.create(product_name=self.product_name, company=self.company)

        with self.assertRaises(IntegrityError):
            # active_component can be null on database
            Product.objects.create(product_name=self.product_name, company=self.company)

    def test_active_component_can_be_set_one(self):

        # active_component can be null on database
        p = Product.objects.create(product_name=self.product_name, company=self.company)

        active_component_list = self.make_active_component_list(1)

        p.active_component.set(active_component_list)

    def test_active_component_can_be_set_multiple(self):

        # active_component can be null on database
        p = Product.objects.create(product_name=self.product_name, company=self.company)

        active_component_list = self.make_active_component_list(3)

        p.active_component.set(active_component_list)


class DrugUseTestCase(TestCase):

    def setUp(self):

        self.mode_of_use = get_random_string(8)

    def test_drug_use_class_works(self):

        try:
            DrugUse.objects.create(mode_of_use=self.mode_of_use)
        except IntegrityError as e:
            self.fail(e)

    def test_mode_of_use_is_required(self):

        with self.assertRaises(IntegrityError):
            DrugUse.objects.create(mode_of_use=None)

    def test_mode_of_use_is_unique(self):

        DrugUse.objects.create(mode_of_use=self.mode_of_use)

        with self.assertRaises(IntegrityError):
            DrugUse.objects.create(mode_of_use=self.mode_of_use)


class SheepDrugTypeTestCase(TestCase):

    def setUp(self):

        self.group = get_random_string(8)
        self.label = get_random_string(8)
        self.colour = get_random_string(8)

    def test_sheep_drug_type_class_works(self):

        try:
            SheepDrugType.objects.create(group=self.group, label=self.label, colour=self.colour)
        except IntegrityError as e:
            self.fail(e)

    def test_group_can_be_null(self):
        """
        needs to be able to be null for SheepDrug model integrity
        """

        try:
            SheepDrugType.objects.create(group=None, label=self.label, colour=self.colour)
        except IntegrityError as e:
            self.fail(e)


class SheepPathogenTestCase(TestCase):

    def setUp(self):

        self.name = get_random_string(8)

    def test_sheep_pathogen_class_works(self):

        try:
            SheepPathogen.objects.create(name=self.name)
        except IntegrityError as e:
            self.fail(e)

    def test_name_is_required(self):

        with self.assertRaises(IntegrityError):
            SheepPathogen.objects.create(name=None)

    def test_name_is_unique(self):

        SheepPathogen.objects.create(name=self.name)

        with self.assertRaises(IntegrityError):
            SheepPathogen.objects.create(name=self.name)


class SheepDrugTestCase(TestCase):

    def setUp(self):

        # generate type fields
        self.group = get_random_string(8)
        self.label = get_random_string(8)
        self.colour = get_random_string(8)
        # create type object
        SheepDrugType.objects.create(group=self.group, label=self.label, colour=self.colour)
        # get type object
        self.type = SheepDrugType.objects.get(group=self.group, label=self.label, colour=self.colour)

        # generate product fields
        # active_component can be null on database
        self.product_name = get_random_string(8)
        company = get_random_string(8)
        Company.objects.create(company=company)
        self.company = Company.objects.get(company=company)
        # create product object
        Product.objects.create(product_name=self.product_name, company=self.company)
        # get product object
        self.product = Product.objects.get(product_name=self.product_name, company=self.company)

        # generate mode_of_use fields
        self.mode_of_use = get_random_string(8)
        # create mode_of_use object
        DrugUse.objects.create(mode_of_use=self.mode_of_use)
        # get mode_of_use object
        self.mode_of_use = DrugUse.objects.get(mode_of_use=self.mode_of_use)

        # get trace_elements
        self.trace_elements = get_random_string(8)

        # get meat_withdrawl_period
        self.meat_withdrawl_period = random.randint(1, 200)

    def make_target_pathogens_list(self, length):

        target_pathogens_list = list()
        for _ in range(length):
            name = get_random_string(8)
            SheepPathogen.objects.create(name=name)
            sp = SheepPathogen.objects.get(name=name)
            target_pathogens_list.append(sp)

        return target_pathogens_list

    def test_sheep_drug_class_works(self):

        try:
            # target_pathogens can be null on database
            SheepDrug.objects.create(type=self.type, product=self.product, mode_of_use=self.mode_of_use, trace_elements=self.trace_elements, meat_withdrawl_period=self.meat_withdrawl_period)
        except IntegrityError as e:
            self.fail(e)

    def test_type_can_be_null(self):

        try:
            # target_pathogens can be null on database
            SheepDrug.objects.create(type=None, product=self.product, mode_of_use=self.mode_of_use, trace_elements=self.trace_elements, meat_withdrawl_period=self.meat_withdrawl_period)
        except IntegrityError as e:
            self.fail(e)

    def test_target_pathogens_can_be_set_one(self):

        # target_pathogens can be null on database
        sd = SheepDrug.objects.create(type=None, product=self.product, mode_of_use=self.mode_of_use, trace_elements=self.trace_elements, meat_withdrawl_period=self.meat_withdrawl_period)

        target_pathogens_list = self.make_target_pathogens_list(1)

        sd.target_pathogens.set(target_pathogens_list)

    def test_target_pathogens_can_be_set_multiple(self):

        # target_pathogens can be null on database
        sd = SheepDrug.objects.create(type=None, product=self.product, mode_of_use=self.mode_of_use, trace_elements=self.trace_elements, meat_withdrawl_period=self.meat_withdrawl_period)

        target_pathogens_list = self.make_target_pathogens_list(3)

        sd.target_pathogens.set(target_pathogens_list)
