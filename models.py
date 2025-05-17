from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, PrimaryKeyConstraint, String, Date, Numeric, Time, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    gender = Column(String)
    age = Column(Integer)
    registered_at = Column(DateTime, default=datetime.now())
    swimming_minutes = Column(Integer)
    notes = Column(Text)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)

    bookings = relationship("Booking", back_populates="customer")
    group_members = relationship("GroupMember", back_populates="customer", cascade="all, delete-orphan")
    user = relationship("User", back_populates="customer", uselist=False)

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    booking_time = Column(TIMESTAMP, server_default=func.now())
    booking_date = Column(Date, nullable=False)
    slot_start = Column(Time, nullable=False)
    slot_end = Column(Time, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    food_order = Column(Text)
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), default="pending")
    band_color = Column(String(20))
    deleted = Column(Boolean, default=False)

    # Relationship with Customer table
    customer = relationship('Customer', back_populates='bookings')
    group_members = relationship("GroupMember", back_populates="booking", cascade="all, delete-orphan")

class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        PrimaryKeyConstraint('booking_id', 'member_id'),
    )

    member_id = Column(Integer, nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"))
    full_name = Column(String(100), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    age = Column(Integer,nullable=True,default=0)
    gender = Column(String(10),nullable=True)

    needs_swimwear = Column(Boolean, default=False)
    swimwear_type = Column(String(20))
    swimwear_cost = Column(Numeric(10, 2), default=0.00)

    needs_tube = Column(Boolean, default=False)
    tube_cost = Column(Numeric(10, 2), default=0.00)

    needs_cap = Column(Boolean, default=False)
    cap_cost = Column(Numeric(10, 2), default=0.00)

    needs_goggles = Column(Boolean, default=False)
    goggles_cost = Column(Numeric(10, 2), default=0.00)
    special_notes = Column(Text)

    # Relationships
    customer = relationship("Customer",uselist=True, back_populates="group_members", lazy="joined")
    booking = relationship("Booking", back_populates="group_members", lazy="joined")

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"))
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_amount = Column(Numeric(10, 2), nullable=False)
    swimming_amount = Column(Numeric(10, 2))
    rental_amount = Column(Numeric(10, 2))
    payment_method = Column(String(50))  # e.g., cash, card, online
    payment_status = Column(String(20), default="pending")  # pending, completed, failed
    transaction_id = Column(String(100), unique=True)
    notes = Column(Text)
    is_deleted = Column(Boolean, default=False)

class MonthlyPackage(Base):
    __tablename__ = "monthly_packages"

    package_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Integer, CheckConstraint("discount_percentage >= 0 AND discount_percentage <= 100"))
    package_status = Column(String(20), default="active")  # active, expired, cancelled

class BlockedDate(Base):
    __tablename__ = "blocked_dates"

    blocked_id = Column(Integer, primary_key=True, index=True)
    blocked_date = Column(Date, nullable=False)
    start_time = Column(Time)  # Nullable if whole day is blocked
    end_time = Column(Time)
    reason = Column(Text)

class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    customer = relationship("Customer", back_populates="user", uselist=False)

