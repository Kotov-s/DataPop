import pandas as pd
import numpy as np
from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split, cross_val_score
import datetime
import os
from matplotlib import pyplot as plt
from matplotlib import cm
import seaborn as sns
from io import StringIO
from contextlib import redirect_stdout
import re
import csv
from django.conf import settings
import shutil

def open_file(path_to_csv):
    try:
        return pd.read_csv(path_to_csv, sep=None, engine='python', header=0,
                        encoding='windows-1251')
    except:
        return pd.read_csv(path_to_csv, sep=None, engine='python', header=0)

def info_to_df(df):
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    lines = info_str.split('\n')
    data = []
    for line in lines[3:-3]:
        match = re.match(r'\s*\d+\s+(.+?)\s+(\d+)\s+non-null\s+(\S+)', line)
        if match:
            col_name = match.group(1).strip()
            non_null_count = match.group(2).strip()
            dtype = match.group(3).strip()
            data.append([col_name, non_null_count, dtype])
    info_df = pd.DataFrame(data, columns=['Column', 'Non-Null Count', 'Dtype'])
    return info_df

def first_analysis_file(path_to_csv, path_to_html):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        f.write(f'<p>Так выглядят первые три строки вашей таблицы:</p>')
        # Записываем таблицу в строку
        table_str = StringIO()
        df[:3].to_html(buf=table_str, border=0,
                       classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        # Добавляем строку с таблицей в файл
        f.write(table_str.getvalue())
        f.write(
            f'\n<p><strong>В вашей таблице {df.shape[0]} записи и {df.shape[1]} столбец (признак).</strong></p>')
        f.write('<p class="font-weight-light">Краткая сводка статистических данных о числовых столбцах в вашем файле. Это может помочь вам быстро понять распределение данных и выявить любые аномалии. Например, чтобы увидеть среднюю цену продажи, минимальную и максимальную цену продажи и другие сводные данные.</p>')

        # Очищаем содержимое объекта StringIO
        table_str.seek(0)
        table_str.truncate(0)

        # Записываем вторую таблицу в строку
        df.describe().to_html(buf=table_str, border=0,
                              classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        f.write(table_str.getvalue())
        f.write('<p class="font-weight-light">Информация о таблице, включая тип индекса и столбцы, ненулевые значения и использование памяти.</p>')

        info_df = info_to_df(df)
        table_str.seek(0)
        table_str.truncate(0)
        info_df.to_html(buf=table_str, border=0,
                        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        # Добавляем строку с таблицей в файл
        f.write(table_str.getvalue())

        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        lines = info_str.split('\n')
        dtypes_line = lines[-3]
        f.write(f'<p><strong>{dtypes_line}</strong></p>')

        f.write('<p>Таблица содержащая количество пропущенных значений для каждого столбца в вашем файле. Это может быть полезно для быстрого обзора количества пропущенных данных в вашем наборе данных.</p>')

        table_str.seek(0)
        table_str.truncate(0)        
        df.isna().sum().to_frame().to_html(buf=table_str, border=0,
                                    classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        
        f.write(table_str.getvalue())


def heat_map(path_to_csv, path_to_html):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        # выбираем только числовые столбцы
        df_numeric = df.select_dtypes(include=['int', 'float'])
        
        if df_numeric.empty:
            f.write('<p class="badge text-bg-danger">В вашем файле нет числовых столбцов из которых можно построить тепловую карту проанализировать.</p>')
        else:
            corr = df_numeric.corr()
            df_styled = corr.style.background_gradient(cmap ='coolwarm')
            df_styled.to_html(path_to_html)

def all_rows(path_to_csv, path_to_html):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        table_str = StringIO()
        f.write('<div style="height: 500px;">')
        df.to_html(buf=table_str, border=0,
                       classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate', )
        f.write(table_str.getvalue())
        f.write('</div>')

def object_statistics(path_to_csv, path_to_html):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        table_str = StringIO()
        f.write('<p>Cводная статистика для всех столбцов типа object в вашем файле</p>')
        df.describe(include=['object']).to_html(buf=table_str, border=0,
                       classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate', )
        f.write(table_str.getvalue())

def drop_na(path_to_csv, path_to_html):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        if df.isna().any().any():
            df = df.dropna(axis='index', how='any')
            df.to_csv(path_to_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)
            table_str = StringIO()
            f.write('<p>Теперь в вашем файле нет отстутвующих элементов. Так выглядит таблица содержащая количество пропущенных значений</p>')
            f.write('<p>Удалены строки, содержащих хотя бы одно значение NaN (NaN означает “Not a Number” (не число) и используется для обозначения отсутствующих или неопределенных значений в числовых данных).</p>')
            f.write('<p class="badge text-bg-danger">Ваш CSV файл обновлен.</p>')
            df.isna().sum().to_frame().to_html(buf=table_str, border=0, classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
            f.write(table_str.getvalue())
        else:
            f.write('<p class="badge text-bg-danger">Нет NaN в вашем файле.</p>')
            
def get_columns(path_to_csv):
    df = open_file(path_to_csv)
    df.columns
    csv_columns = []
    for column in df.columns:
        csv_columns.append(column)
    return csv_columns

def delete_column(path_to_csv, path_to_html, column_name):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = open_file(path_to_csv)
        df = df.drop(columns=[column_name])
        df.to_csv(path_to_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)
        table_str = StringIO()
        f.write(f'<p class="badge text-bg-danger">Столбец <strong>{column_name}</strong> удален</p>')
        columns_df = pd.DataFrame(df.columns)
        columns_df.to_html(buf=table_str, border=0,
                           classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        f.write(table_str.getvalue())

def boxplot_graph(path_to_csv, path_to_html, path_to_png_dir):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        df = pd.read_csv(path_to_csv)
        img_folder_path = os.path.join(settings.BASE_DIR / "chat/static/chat", path_to_png_dir)
        os.makedirs(img_folder_path, exist_ok=True)
        if (not df.select_dtypes(include=['int', 'float']).empty):
            for col in df.select_dtypes(include=['float64', 'int64']).columns:
                plt.figure(figsize=(16,2))
                sns.boxplot(data=df[[col]], orient='h')
                now = datetime.datetime.now()
                formatted_time = now.strftime('%Y%m%d%H%M%S%f')
                png_name = f'{col}boxplot{formatted_time}.png'
                plt.savefig(os.path.join(img_folder_path, png_name))
                f.write(f'<img class="img-fluid w-75" src="/static/chat/{path_to_png_dir}\{png_name}" alt="{col}">\n')
                f.write(f'<p class="m-3 text-center">Ящик с усами для столбца <strong>{col}</strong></p>\n')
        else:
            f.write(f'<p class="badge text-bg-danger">В вашем файле нет числовых столбцов. Невозможно построить язики с усами</p>\n')

def back_to_roots(path_to_edited_csv, path_to_original_csv, path_to_html):
    shutil.copyfile(path_to_original_csv, path_to_edited_csv)
    with open(path_to_html, 'a', encoding='utf-8') as f:
        f.write(f'<p class="badge text-bg-danger" >Файл возвращен в исходную позицию</p>')


def pie_plot(path_to_csv, path_to_html, column_name, path_to_png_dir):
    df = pd.read_csv(path_to_csv)
    df = df.dropna(axis='index', how='any')
    img_folder_path = os.path.join(settings.BASE_DIR / "chat/static/chat", path_to_png_dir)
    os.makedirs(img_folder_path, exist_ok=True)
    
    with open(path_to_html, 'a', encoding='utf-8') as f:
        try:
            df = open_file(path_to_csv)
            counts = df[f'{column_name}'].value_counts()
            plt.figure(figsize=(5, 5))
            plt.clf()
            plt.pie(counts, labels=counts.index)

            now = datetime.datetime.now()
            formatted_time = now.strftime('%Y_%m_%d_%H_%M_%S_%f')
            png_name = f'pie_plot_{formatted_time}.png'
            plt.savefig(os.path.join(img_folder_path, png_name), dpi=300)
            
            f.write(f'<img class="img-fluid w-50" src="/static/chat/{path_to_png_dir}\{png_name}" alt="Pie plot">\n')
        except:
            f.write(f'<p class="badge text-bg-danger">Не удалось построить диаграмму</p>\n')
