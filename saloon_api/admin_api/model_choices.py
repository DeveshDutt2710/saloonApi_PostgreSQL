PROFILE_TYPE_VENDOR = "vendor"
PROFILE_TYPE_CUSTOMER = 'customer'
PROFILE_TYPE_ADMIN = 'admin'

PROFILE_TYPE = (
    (PROFILE_TYPE_VENDOR, "vendor"),
    (PROFILE_TYPE_CUSTOMER, "customer"),
    (PROFILE_TYPE_ADMIN, "admin")
)

PROFILE_GENDER_MALE = "male"
PROFILE_GENDER_FEMALE = "female"

PROFILE_GENDER = (
    (PROFILE_GENDER_MALE, "male"),
    (PROFILE_GENDER_FEMALE, "female")
)

PRODUCT_CATEGORY_CUTLERY = "cutlery"
PRODUCT_CATEGORY_MEDICINES = 'medicines'
PRODUCT_CATEGORY_FURNITURES = 'furnitures'
PRODUCT_CATEGORY_ELECTRONICS = 'electronics'

PRODUCT_CATEGORIES = (
    (PRODUCT_CATEGORY_ELECTRONICS, 'electronics'),
    (PRODUCT_CATEGORY_FURNITURES, 'furnitures'),
    (PRODUCT_CATEGORY_MEDICINES, 'medicines'),
    (PRODUCT_CATEGORY_CUTLERY, "cutlery")
)

PRODUCT_TYPE_PRODUCT = "product"
PRODUCT_TYPE_SERVICE = 'service'

PRODUCT_TYPES = (
    (PRODUCT_TYPE_PRODUCT, "product"),
    (PRODUCT_TYPE_SERVICE, "service")
)


ORDER_STATUS_COMPLETED = "completed"
ORDER_STATUS_UPCOMING = 'upcoming'
ORDER_STATUS_CANCELLED = 'cancelled'

ORDER_STATUS = (
    (ORDER_STATUS_COMPLETED, "completed"),
    (ORDER_STATUS_UPCOMING, "upcoming"),
    (ORDER_STATUS_CANCELLED, "cancelled")
)

PAYMENT_STATUS_SUCCESSFULL = "successful"
PAYMENT_STATUS_PENDING = 'pending'

PAYMENT_STATUS = (
    (PAYMENT_STATUS_SUCCESSFULL, "successful"),
    (PAYMENT_STATUS_PENDING, "pending")
)