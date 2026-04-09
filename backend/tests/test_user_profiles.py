# from app.models import CustomerProfile, DelivererProfile, User


# def test_users_seeded(db_session):
#     """
#     Template test for seeded users.

#     This verifies that the DB setup step inserted the expected example users.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     If seed_test_data() changes usernames, user count, or required user fields,
#     update this test accordingly.
#     """
#     users = db_session.query(User).all()

#     assert len(users) == 2

#     usernames = [user.username for user in users]
#     assert "alice" in usernames
#     assert "bob" in usernames


# def test_customer_profile_seeded(db_session):
#     """
#     Template test for the customer profile relationship.

#     This verifies that:
#     - the sample customer user exists
#     - the user does not have a deliverer profile
#     - the customer profile is linked correctly

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     Update this if the customer/user relationship changes.
#     """
#     user = db_session.query(User).filter(User.username == "alice").first()

#     assert user is not None
#     assert user.has_deliverer_profile is False
#     assert user.customer_profile is not None
#     assert user.customer_profile.user_id == user.id


# def test_deliverer_profile_seeded(db_session):
#     """
#     Template test for the deliverer profile relationship.

#     This verifies that:
#     - the sample deliverer user exists
#     - the user is marked as a deliverer
#     - the deliverer profile link is present

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     Update this if the deliverer/user relationship changes.
#     """
#     user = db_session.query(User).filter(User.username == "bob").first()

#     assert user is not None
#     assert user.has_deliverer_profile is True
#     assert user.deliverer_id is not None
#     assert user.deliverer_profile is not None


# def test_profile_tables_have_rows(db_session):
#     """
#     Template sanity check for seeded profile tables.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     If seed counts change, update the expected row counts here.
#     """
#     customer_profiles = db_session.query(CustomerProfile).all()
#     deliverer_profiles = db_session.query(DelivererProfile).all()

#     assert len(customer_profiles) == 1
#     assert len(deliverer_profiles) == 1
