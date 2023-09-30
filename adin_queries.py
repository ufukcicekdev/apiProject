 
# sql_queries.py
SELECT_ALL_DOMAINS_DATA = "SELECT * FROM adin_telecommunication_product_detail;"
SELECT_DATA_BY_DATE = "SELECT * FROM adin_telecommunication_product_detail WHERE create_date BETWEEN %s AND %s AND domain_id = %s;"
SELECT_DATA_BY_CREATEDATE = "SELECT * FROM adin_telecommunication_product_detail WHERE create_date = %s"
SELECT_DATA_BY_CREATEDATE_DOMAINID = "SELECT * FROM adin_telecommunication_product_detail WHERE create_date = %s and domain_id = %s;"



