from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils import timezone
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import os
import glob

def _get_files(filepath: str):
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.csv"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


with DAG(
    "etl",
    start_date=timezone.datetime(2024,5,4),
    schedule_interval="@daily",
    tags=["swu"],
) as dag:

# Dummy strat task   
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )


    # Task to load data into Google Cloud Storage
    upload_file_customers_to_capstone = GCSToGCSOperator(
        task_id="upload_file_customers_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_customers_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_customers_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_geolocation_to_capstone = GCSToGCSOperator(
        task_id="upload_file_geolocation_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_geolocation_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_geolocation_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_items_to_capstone = GCSToGCSOperator(
        task_id="upload_file_items_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_order_items_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_order_items_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_payments_to_capstone = GCSToGCSOperator(
        task_id="upload_file_payments_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_order_payments_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_order_payments_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_reviews_to_capstone = GCSToGCSOperator(
        task_id="upload_file_reviews_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_order_reviews_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_order_reviews_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_orders_to_capstone = GCSToGCSOperator(
        task_id="upload_file_orders_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_orders_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_orders_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_products_to_capstone = GCSToGCSOperator(
        task_id="upload_file_products_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_products_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_products_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )
    upload_file_sellers_to_capstone = GCSToGCSOperator(
        task_id="upload_file_sellers_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["olist_sellers_dataset.csv"],
        destination_bucket="storage-capstone",
        destination_object="olist_sellers_dataset.csv",
        gcp_conn_id='my_gcp_conn'
    )

    upload_file_name_to_capstone = GCSToGCSOperator(
        task_id="upload_file_name_to_capstone",
        source_bucket="raw_data_projectcapstone",
        source_objects=["product_category_name_translation.csv"],
        destination_bucket="storage-capstone",
        destination_object="product_category_name_translation.csv",
        gcp_conn_id='my_gcp_conn'
    )
#------------------------------------------------------------------------------------------------------#

    create_order_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_order_dataset',
        dataset_id='order',
        gcp_conn_id='my_gcp_conn',
    )

#-----------------------------------------------------------------------------------------------------#

    gcs_to_bq_customers = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_customers",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_customers_dataset.csv'],
    destination_project_dataset_table   ='order.olist_customers_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_geolocation = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_geolocation",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_geolocation_dataset.csv'],
    destination_project_dataset_table   ='order.olist_geolocation_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_items = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_items",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_order_items_dataset.csv'],
    destination_project_dataset_table   ='order.olist_items_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_payments = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_payments",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_order_payments_dataset.csv'],
    destination_project_dataset_table   ='order.olist_payments_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_reviews = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_reviews",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_order_reviews_dataset.csv'],
    destination_project_dataset_table   ='order.olist_reviews_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_orders = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_orders",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_orders_dataset.csv'],
    destination_project_dataset_table   ='order.olist_orders_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_products = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_products",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_products_dataset.csv'],
    destination_project_dataset_table   ='order.olist_products_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_sellers = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_sellers",
    bucket                              = 'storage-capstone',
    source_objects                      = ['olist_sellers_dataset.csv'],
    destination_project_dataset_table   ='order.olist_sellers_dataset',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_to_bq_translation = GCSToBigQueryOperator(
    task_id                             = "gcs_to_bq_translation",
    bucket                              = 'storage-capstone',
    source_objects                      = ['product_category_name_translation.csv'],
    destination_project_dataset_table   ='order.product_category_name_translation',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )


# Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag,
    )

    # start >> get_files >> upload_file >> create_order_dataset >> load_dataset_order >> transform_bq >> end
    # start >> get_files >> [upload_file_customers, upload_file_geolocation, upload_file_items, upload_file_name ,upload_file_orders, upload_file_payments, upload_file_products, upload_file_reviews, upload_file_sellers] >> create_order_dataset >> [gcs_to_bq_customers, gcs_to_bq_geolocation, gcs_to_bq_items, gcs_to_bq_orders, gcs_to_bq_payments, gcs_to_bq_products, gcs_to_bq_reviews, gcs_to_bq_sellers, gcs_to_bq_translation]
    start >> [upload_file_customers_to_capstone, upload_file_geolocation_to_capstone, upload_file_items_to_capstone, upload_file_name_to_capstone ,upload_file_orders_to_capstone, upload_file_payments_to_capstone, upload_file_products_to_capstone, upload_file_reviews_to_capstone, upload_file_sellers_to_capstone] >> create_order_dataset >> [gcs_to_bq_customers, gcs_to_bq_geolocation, gcs_to_bq_items, gcs_to_bq_orders, gcs_to_bq_payments, gcs_to_bq_products, gcs_to_bq_reviews, gcs_to_bq_sellers, gcs_to_bq_translation] >> end
