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
import plotly.express as px
from statsmodels.graphics.mosaicplot import mosaic
from scipy.cluster.hierarchy import dendrogram, linkage


def open_file(path_to_csv):
    try:
        return pd.read_csv(path_to_csv, sep=',', engine='python', header=0,
                        encoding='windows-1251', na_values=[''])
    except:
        return pd.read_csv(path_to_csv, sep=',', engine='python', header=0, na_values=[''])


def get_columns(path_to_csv):
    df = open_file(path_to_csv)
    df.columns
    csv_columns = []
    for column in df.columns:
        csv_columns.append(column)
    return csv_columns


def save_plot_and_update_html(plt, path_to_png_dir, path_to_html, plot_type):
    img_folder_path = os.path.join(settings.BASE_DIR / "chat/static/chat", path_to_png_dir)
    os.makedirs(img_folder_path, exist_ok=True)
    now = datetime.datetime.now()
    formatted_time = now.strftime('%Y%m%d%H%M%S%f')
    png_name = f'{plot_type}{formatted_time}.png'
    plt.savefig(os.path.join(img_folder_path, png_name))
    write_html_content(path_to_html, f'<img id="img-chart" class="mx-auto d-flex" src="/static/chat/{path_to_png_dir}\{png_name}" alt="{plot_type}">\n')


def write_html_content(path_to_html, content):
    with open(path_to_html, 'a', encoding='utf-8') as f:
        f.write(content)


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


def find_state_column(columns):
    i = 0
    for column in columns:
        l_col = column.lower()
        if 'state' in l_col or 'province' in l_col or 'territory' in l_col or 'code' in l_col:
            return column, columns[:i] + columns[i+1:]
        i += 1
    return columns[0], columns[1:]


def show_nans(path_to_csv, path_to_html):
    table_str = StringIO()
    df = open_file(path_to_csv)
    write_html_content(path_to_html, '<p>Таблица содержащая количество пропущенных значений для каждого столбца в вашем файле. Это может быть полезно для быстрого обзора количества пропущенных данных в вашем наборе данных.</p>')

    table_str.seek(0)
    table_str.truncate(0)        
    df.isna().sum().to_frame().to_html(buf=table_str, border=0,
                                classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
    
    write_html_content(path_to_html, table_str.getvalue())


def first_analysis_file(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        write_html_content(path_to_html, f'<p>Так выглядят первые три строки вашей таблицы:</p>')
        # Записываем таблицу в строку
        table_str = StringIO()
        df[:3].to_html(buf=table_str, border=0,
                        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        # Добавляем строку с таблицей в файл
        write_html_content(path_to_html, table_str.getvalue())
        write_html_content(path_to_html, 
            f'\n<p><strong>В вашей таблице {df.shape[0]} записи и {df.shape[1]} столбец (признак).</strong></p>')
        write_html_content(path_to_html, '<p class="font-weight-light">Краткая сводка статистических данных о числовых столбцах в вашем файле. Это может помочь вам быстро понять распределение данных и выявить любые аномалии. Например, чтобы увидеть среднюю цену продажи, минимальную и максимальную цену продажи и другие сводные данные.</p>')

        # Очищаем содержимое объекта StringIO
        table_str.seek(0)
        table_str.truncate(0)

        # Записываем вторую таблицу в строку
        df.describe().to_html(buf=table_str, border=0,
                                classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        write_html_content(path_to_html, table_str.getvalue())
        write_html_content(path_to_html, '<p class="font-weight-light">Информация о таблице, включая тип индекса и столбцы, ненулевые значения и использование памяти.</p>')

        info_df = info_to_df(df)
        table_str.seek(0)
        table_str.truncate(0)
        info_df.to_html(buf=table_str, border=0,
                        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        # Добавляем строку с таблицей в файл
        write_html_content(path_to_html, table_str.getvalue())

        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        lines = info_str.split('\n')
        dtypes_line = lines[-3]
        write_html_content(path_to_html, f'<p><strong>{dtypes_line}</strong></p>')

        show_nans(path_to_csv, path_to_html)
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def heat_map(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        # выбираем только числовые столбцы
        df_numeric = df.select_dtypes(include=['int', 'float'])
        
        if df_numeric.empty:
            write_html_content(path_to_html, '<p class="badge text-bg-danger">В вашем файле нет числовых столбцов из которых можно построить тепловую карту проанализировать.</p>')
        else:
            corr = df_numeric.corr()
            df_styled = corr.style.background_gradient(cmap ='coolwarm')
            df_styled.to_html(path_to_html)
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def all_rows(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        table_str = StringIO()
        write_html_content(path_to_html, '<div style="height: 500px;">')
        df.to_html(buf=table_str, border=0,
                        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate', )
        write_html_content(path_to_html, table_str.getvalue())
        write_html_content(path_to_html, '</div>')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def object_statistics(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        table_str = StringIO()
        write_html_content(path_to_html, '<p>Cводная статистика для всех столбцов типа object в вашем файле</p>')
        df.describe(include=['object']).to_html(buf=table_str, border=0,
                        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate', )
        write_html_content(path_to_html, table_str.getvalue())
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def drop_na(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        if df.isna().any().any():
            df = df.dropna(axis='index', how='any')
            df.to_csv(path_to_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)
            show_nans(path_to_csv, path_to_html)
        else:
            write_html_content(path_to_html, '<p class="badge text-bg-danger">Нет NaN в вашем файле.</p>')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def delete_column(path_to_csv, path_to_html, column_name):
    try:
        df = open_file(path_to_csv)

        df = df.drop(columns=column_name)
        df.to_csv(path_to_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)

        table_str = StringIO()
        write_html_content(path_to_html, f'<p class="badge text-bg-danger">Столбец/столбцы удалены</p>')
        columns_df = pd.DataFrame(df.columns)
        columns_df.to_html(buf=table_str, border=0,
                            classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate')
        write_html_content(path_to_html, table_str.getvalue())
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def back_to_roots(path_to_edited_csv, path_to_original_csv, path_to_html):
    try:
        shutil.copyfile(path_to_original_csv, path_to_edited_csv)
        write_html_content(path_to_html, f'<p class="badge text-bg-danger" >Файл возвращен в исходную позицию</p>')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def boxplot_graph(path_to_csv, path_to_html, path_to_png_dir):
    try:
        df = open_file(path_to_csv)
        if (not df.select_dtypes(include=['int', 'float']).empty):
            for col in df.select_dtypes(include=['float64', 'int64']).columns:
                plt.figure(figsize=(16,2))
                sns.boxplot(data=df[[col]], orient='h')
                save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'boxplot_graph') 
                write_html_content(path_to_html, f'<p class="m-3 text-center">Ящик с усами для столбца <strong>{col}</strong></p>\n')
        else:
            write_html_content(path_to_html, f'<p class="badge text-bg-danger">В вашем файле нет числовых столбцов. Невозможно построить ящики с усами</p>\n')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def histogram_graph(path_to_csv, path_to_html, path_to_png_dir):
    try:
        df = open_file(path_to_csv)

        if (not df.select_dtypes(include=['int', 'float']).empty):
            for col in df.select_dtypes(include=['float64', 'int64']).columns:
                plt.figure(figsize=(16,2))
                plt.hist(df[col], bins=30)
                save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'histogram_graph')
                write_html_content(path_to_html, f'<p class="m-3 text-center">Гисторграмма столбца <strong>{col}</strong></p>\n')
        else:
            write_html_content(path_to_html, f'<p class="badge text-bg-danger">В вашем файле нет числовых столбцов. Невозможно построить гисторграммы</p>\n')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def non_object_statistics(path_to_csv, path_to_html):
    try:
        df = open_file(path_to_csv)
        table_str = StringIO()
        write_html_content(path_to_html, '<p>Сводная статистика для всех необъектных столбцов в вашем файле</p>')
        df.describe(exclude=['object']).to_html(buf=table_str, border=0,
        classes='d-block dataframe overflow-auto table table-bordered table-hover table-sm table-striped text-truncate', )
        write_html_content(path_to_html, table_str.getvalue())
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def pie_plot(path_to_csv, path_to_html, column_name, path_to_png_dir):
    try:
        df = open_file(path_to_csv)
        
        df = open_file(path_to_csv)
        counts = df[f'{column_name}'].value_counts()
        plt.figure(figsize=(7, 5))
        plt.clf()
        plt.pie(counts, labels=counts.index)

        save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'pie_plot')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def state_map_plot(path_to_csv, path_to_html, columns, path_to_png_dir):
    try:
        state, other_column =  find_state_column(columns)
        other_column = other_column[0]

        img_folder_path = os.path.join(settings.BASE_DIR / "chat/static/chat", path_to_png_dir)
        os.makedirs(img_folder_path, exist_ok=True)

        df = open_file(path_to_csv)
        fig = px.choropleth(df,
                            locations=state,
                            locationmode="USA-states",
                            scope="usa",
                            color=other_column,
                            color_continuous_scale="Viridis_r")
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y_%m_%d_%H_%M_%S_%f')
        fig.write_image(f'{img_folder_path}/choropleth_map_{formatted_time}.png')

        write_html_content(path_to_html,f'<img class="img-chart" src="/static/chat/{path_to_png_dir}/choropleth_map_{formatted_time}.png" alt="Фоновая картограмма">\n')

    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def bar_plot(path_to_csv, path_to_html, columns, path_to_png_dir):
    try:
        df = open_file(path_to_csv)

        means = df.groupby(columns[0])[columns[1]].mean()
        plt.figure(figsize=(7, 5))
        plt.clf()
        means.plot(kind='bar')
        
        save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'bar_plot')

    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')



def scatter_plot(path_to_csv, path_to_html, columns, path_to_png_dir):
    try:
        x_column, y_column = columns[:2]
        df = open_file(path_to_csv)
        plt.figure(figsize=(7, 5))
        plt.clf()
        plt.scatter(df[x_column], df[y_column])

        save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'scatter_plot')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def group_by_sum(path_to_csv, path_to_html, column):
    try:
        df = open_file(path_to_csv)
        grouped_df = df.groupby(column).sum()
        grouped_df.to_csv(path_to_csv)
        all_rows(path_to_csv, path_to_html)
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')


def group_by_mean(path_to_csv, path_to_html, column):
    try:
        df = open_file(path_to_csv)
        grouped_df = df.groupby(column).mean()
        grouped_df.to_csv(path_to_csv)
        all_rows(path_to_csv, path_to_html)
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить/Это возможно сделать только если у вас есть только столбцы с типом данных "не объект"</p>')


def dendrogram_plot(path_to_csv, path_to_html, columns, path_to_png_dir):
    try:
        df = open_file(path_to_csv)
        x = df[columns[0]].tolist()
        y = df[columns[1]].tolist()

        data = list(zip(x, y))

        linkage_data = linkage(data, method='ward', metric='euclidean')
        plt.figure(figsize=(7, 5))
        plt.clf()        
        dendrogram(linkage_data)

        save_plot_and_update_html(plt, path_to_png_dir, path_to_html, 'hierarchical_clustering_plot')
    except:
        write_html_content(path_to_html, '<p class="badge text-bg-danger">Не удалось выполнить</p>')