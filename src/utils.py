def dms_to_decimal(dms):
    try:
        # Remove directional letters and split the DMS string into components
        dms = dms.strip().upper()  # Ensure consistent formatting
        parts = dms.replace('W', '').replace('E', '').replace('N', '').replace('S', '').split('-')
        
        # Ensure the DMS string has exactly 3 components (degrees, minutes, seconds)
        if len(parts) != 3:
            raise ValueError(f"Invalid DMS format: {dms}")

        degrees, minutes, seconds = [float(x) for x in parts]
        
        # Convert to decimal degrees
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        
        # Handle negative values for west and south coordinates
        if 'W' in dms or 'S' in dms:
            decimal = -decimal
        
        return decimal
    except Exception as e:
        print(f"Error converting DMS to decimal: {e}")
        return None  # Return None for invalid DMS strings
