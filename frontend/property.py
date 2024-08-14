import pandas as pd
import streamlit as st

from property_tracker.models.property import Property, PropertyType, Status
from property_tracker.repositories import PropertyRepository
from property_tracker.services import PropertyService


def show_properties(session):
    property_service = PropertyService(PropertyRepository(session))

    st.write("### Properties")
    inv_properties = property_service.get_all_properties()
    inv_properties_df = pd.DataFrame([inv_property.__dict__ for inv_property in inv_properties])
    st.dataframe(inv_properties_df, hide_index=True)

    st.write("### Add New Property")
    with st.form(key="property_form"):
        address = st.text_input("Address")
        postcode = st.text_input("Postcode")
        city = st.text_input("City")
        description = st.text_area("Description")
        no_of_bedrooms = st.number_input("Number of Bedrooms", min_value=1, step=1)
        no_of_bathrooms = st.number_input("Number of Bathrooms", min_value=1, step=1)
        sqm = st.number_input("Square Meters", min_value=1.0, step=0.1)
        floor = st.number_input("Floor", min_value=0, step=1)
        furnished = st.checkbox("Furnished")
        property_type = st.selectbox("Property Type", [property_type.value for property_type in PropertyType])
        status = st.selectbox("Status", [status.value for status in Status])
        submit_button = st.form_submit_button(label="Add Property")

        if submit_button:
            property_service.create_property(
                address=address,
                postcode=postcode,
                city=city,
                description=description,
                no_of_bedrooms=no_of_bedrooms,
                no_of_bathrooms=no_of_bathrooms,
                sqm=sqm,
                floor=floor,
                furnished=furnished,
                property_type=PropertyType(property_type),
                status=Status(status),
            )
            st.success("Property added successfully!")
