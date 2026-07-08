import click
import os
import sys

# Устанавливаем UTF-8 для вывода в консоль Windows
sys.stdout.reconfigure(encoding='utf-8')

class RussianHelpGroup(click.Group):
    def format_help(self, ctx: click.Context, formatter):
        # Заголовок "Использование:"
        formatter.write_heading("Использование:")
        formatter.write_text(f"  {self.get_usage(ctx)}")
        formatter.write_text("")

        # Опции 
        formatter.write_heading("Опции:")
        formatter.write_text("  --help  Показать это сообщение и выйти.")
        formatter.write_text("")

        # Команды
        if self.commands:
            formatter.write_heading("Команды:")
            self._format_commands(ctx, formatter)
            formatter.write_text("")

    def _format_commands(self, ctx, formatter):
        """Форматирует список команд с русскими описаниями"""
        commands = []
        for name, command in self.commands.items():
            if name == "help":
                continue
            help_text = command.help or ""
            commands.append((name, help_text))
        if commands:
            commands.sort()
            for name, help_text in commands:
                formatter.write_text(f"  {name:<10} {help_text}")

    # Отключаем автоматическое добавление стандартной опции --help
    def get_help_options(self, ctx):
        return []


# Основная группа команд с русской справкой
@click.group(cls=RussianHelpGroup)
@click.pass_context
def todo(ctx):
    '''Простое CLI-приложение для списка задач'''
    ctx.ensure_object(dict)
    if not os.path.exists('./todo.txt') or os.path.getsize('./todo.txt') == 0:
        with open('./todo.txt', 'w') as f:
            f.write('0\n')
        ctx.obj['LATEST'] = 0
        ctx.obj['TASKS'] = {}
        return

    with open('./todo.txt', 'r') as f:
        content = f.readlines()
    
    if not content:
        ctx.obj['LATEST'] = 0
        ctx.obj['TASKS'] = {}
        return

    try:
        ctx.obj['LATEST'] = int(content[0].strip())
    except ValueError:
        ctx.obj['LATEST'] = 0

    ctx.obj['TASKS'] = {}
    for line in content[1:]:
        line = line.strip()
        if not line:
            continue
        if '|||' in line:
            task_id, task_text = line.split('|||', 1)
            ctx.obj['TASKS'][task_id] = task_text


@todo.command()
@click.pass_context
def tasks(ctx):
    '''Показать все задачи'''
    if ctx.obj['TASKS']:
        click.echo('ВАШИ ЗАДАЧИ\n**********')
        for i, task in ctx.obj['TASKS'].items():
            click.echo(f'• {task} (ID: {i})')
        click.echo('')
    else:
        click.echo('Задач пока нет. Используйте ADD для добавления.\n')


@todo.command()
@click.pass_context
@click.option('-add', '--add_task', prompt='Введите задачу для добавления')
def add(ctx, add_task):
    '''Добавить новую задачу'''
    add_task = add_task.strip()
    if not add_task:
        click.echo(' Задача не может быть пустой.')
        return

    new_id = str(ctx.obj['LATEST'])
    ctx.obj['TASKS'][new_id] = add_task
    click.echo(f' Добавлена задача "{add_task}" с ID {new_id}')

    new_latest = ctx.obj['LATEST'] + 1
    with open('./todo.txt', 'w') as f:
        f.write(f'{new_latest}\n')
        for tid, ttext in ctx.obj['TASKS'].items():
            f.write(f'{tid}|||{ttext}\n')
    ctx.obj['LATEST'] = new_latest


@todo.command()
@click.pass_context
@click.option('-fin', '--fin_taskid', prompt='Введите ID задачи для завершения', type=int)
def done(ctx, fin_taskid):
    '''Завершить (удалить) задачу по ID'''
    key = str(fin_taskid)
    if key not in ctx.obj['TASKS']:
        click.echo(f'❌ Ошибка: задача с ID {fin_taskid} не найдена.')
        return

    task_text = ctx.obj['TASKS'].pop(key)
    click.echo(f' Завершена и удалена задача "{task_text}" с ID {fin_taskid}')

    if ctx.obj['TASKS']:
        with open('./todo.txt', 'w') as f:
            f.write(f'{ctx.obj["LATEST"]}\n')
            for tid, ttext in ctx.obj['TASKS'].items():
                f.write(f'{tid}|||{ttext}\n')
    else:
        ctx.obj['LATEST'] = 0
        with open('./todo.txt', 'w') as f:
            f.write('0\n')


if __name__ == '__main__':
    todo()
