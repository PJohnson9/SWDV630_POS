# Patrick Johnson          5/1/2020 #
# SWDV 630 3W 20/SP2  Final Project #
#####################################
#Point of Sale System - Partial Implementation
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Classes
class Category(Base):
    def __init__(self, description):
        self.description = description
        
    def __str__(self):
        return self.description
    
    __tablename__ = "Categories"
    
    category_id = sa.Column(sa.Integer, primary_key = True)
    description = sa.Column(sa.String)

class Employee(Base):    
    def __init__(self, name, PIN):
        self.name = name
        self.__PIN = PIN
       
    def __repr__(self):
        return "Employee - ID: {}; Name: {}".format(self.employee_id, self.name)
    
    __tablename__ = "Employees"
    employee_id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(24))
    __PIN = sa.Column(sa.String(8))
    employee_type = sa.Column(sa.String(7))
    
    __mapper_args__ = {
        'polymorphic_on':employee_type,
        'polymorphic_identity':'Employee'
    }
        
    def verify_PIN(self, PIN):
        return self.__PIN == PIN
    
    def update_PIN(self, old_PIN, new_PIN):
        if self.verify_PIN(old_PIN):
            self.__PIN = new_PIN
            return True
        else:
            return False
    
class Manager(Employee):
    def __repr__(self):
        return "Manager  - ID: {}; Name: {}".format(self.employee_id, self.name)
    
    __mapper_args__ = {
        'polymorphic_identity':'Manager'
    }

class Clerk(Employee):
    def __repr__(self):
        return "Clerk    - ID: {}; Name: {}".format(self.employee_id, self.name)
    
    __mapper_args__ = {
        'polymorphic_identity':'Clerk'
    }

class Item(Base):
    def __init__(self, barcode, description, category, employee):
        self.barcode = barcode
        self.description = description
        self.category = category
        self.added_by = employee
        
    def __repr__(self):
        return "{} Item - ID: {} Barcode: {}; Category: {}; Description: {}".format(self.type,
                                                                                    self.item_id,
                                                                                    self.barcode,
                                                                                    self.category,
                                                                                    self.description)
    
    __tablename__ = "Items"
    item_id = sa.Column(sa.Integer, primary_key = True)
    barcode = sa.Column(sa.Integer)
    description = sa.Column(sa.String(32))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('Categories.category_id'))
    category = relationship("Category")
    added_by_employee_id = sa.Column(sa.Integer, sa.ForeignKey('Employees.employee_id'))
    add_by = relationship("Employee")
    type = sa.Column(sa.String(10))
    
    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'BaseItem'
    }
    
    def get_price(self):
        pass
        
    price = property(get_price, None, None, "Item Price")
    
    @classmethod
    def get_item_from_barcode(cls, barcode, session):
        return session.query(Item).filter(Item.barcode == barcode).one()

class Fixed_Price_Item(Item):
    def __init__(self, barcode, description, category, employee, price):
        Item.__init__(self, barcode, description, category, employee)
        self._price = price
    
    _price = sa.Column(sa.Float)
    
    __mapper_args__ = {
        'polymorphic_identity':'FixedPrice'
    }
        
    def get_price(self):
        return self._price
    
    price = property(get_price, None, None, "Price")
    
class Per_Unit_Item(Item):
    def __init__(self, barcode, description, category, employee, price, unit):
        Item.__init__(self, barcode, description, category, employee)
        self.unit = unit
        self._unit_price = price
    
    _unit_price = sa.Column(sa.Float)
    unit = sa.Column(sa.String(12))
    __mapper_args__ = {
        'polymorphic_identity':'PerUnit'
    }
    
    def get_price(self):
        return self._unit_price
    
    price = property(get_price, None, None, "Unit Price")
        
class SaleItem(Base):
    def __init__(self, item, quantity, sale):
        self.item = item
        self.quantity = quantity
        self.sale = sale
    
    def __str__(self):
        return "{} - {} @ ${}".format(self.item.description,
                                      self.quantity,
                                      self.item.price)
    
    __tablename__ = "SaleItems"
    sale_item_id = sa.Column(sa.Integer, primary_key = True)
    quantity = sa.Column(sa.Float)
    item_id = sa.Column(sa.Integer, sa.ForeignKey('Items.item_id'))
    item = relationship("Item")
    sale_id = sa.Column(sa.Integer, sa.ForeignKey('Sales.transaction_id'))
    sale = relationship("Sale", back_populates="items")
    
    def get_item_total(self):
        return self.item.price * self.quantity
    
    price = property(get_item_total)

class Sale(Base):
    def __init__(self, employee):
        self.clerk = employee
    
    __tablename__ = "Sales"
    transaction_id = sa.Column(sa.Integer, primary_key = True)
    timestamp = sa.Column(sa.DateTime)
    
    items = relationship("SaleItem", back_populates="sale")    
    clerk_id = sa.Column(sa.Integer, sa.ForeignKey('Employees.employee_id'))
    clerk = relationship("Employee")
    
    def add_item(self, barcode, session, quantity = 1):
        item = Item.get_item_from_barcode(barcode, session)
        saleitem = SaleItem(item, quantity, self)
        
        
    def get_total(self):
        total = 0
        for i in self.items:
            total += i.price
        return total
    
    def finalize(self, session):
        self.timestamp = datetime.now()
        session.commit()
            
def populate_database(session):
    bob = Manager("Bob S.", "1234")
    session.add(bob)
    session.add(Clerk("Ann D.", "0000"))
    session.commit()
    
        # Add a category
    paper_category = Category("Paper Products")
    session.add(paper_category)
    session.commit()
    

    # Create Some Items
    session.add(Fixed_Price_Item(2812, "Notebook", paper_category, bob, 5.99))
    session.add(Per_Unit_Item(4353, "Paper", paper_category, bob, 0.25, "Sheet"))
    session.commit()

def main():
    engine = sa.create_engine("sqlite://", echo = False)
    Base.metadata.create_all(engine)
    session = sa.orm.sessionmaker(bind=engine)()
    
    populate_database(session)  # Adds sample items and users
 
    bob = session.query(Employee).first()

    # Check PINs:
    print("Check incorrect PIN for Bob:", bob.verify_PIN("1111"))
    print("Check correct PIN for Bob:  ", bob.verify_PIN("1234"))

    # Update PIN for Bob
    print("Updating Bob's PIN to '5309':", bob.update_PIN("1234", "5309"))
    print("Check old PIN for Bob:", bob.verify_PIN("1234"))
    print("Check new PIN for Bob:", bob.verify_PIN("5309"))


    # Print Employee List
    print("Employees:")
    for employee in session.query(Employee).all():
        print(employee)

    
    # Create a  Sale
    sale = Sale(bob)  # Generate new sale
    session.add(sale) # Add to session
    sale.add_item(2812, session)    # Add items
    sale.add_item(4353, session, 5)
    sale.finalize(session)
    
    print("Sale Items:")
    for si in sale.items:
        print(si)
    print("Sale Total:", sale.get_total())
    print("Sale Clerk:", sale.clerk)
    print("Sale Time: ", sale.timestamp)
    
    

if __name__ == "__main__":
    main()