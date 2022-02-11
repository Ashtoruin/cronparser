#!/usr/bin/python3
import argparse

# Handle , first as it combines other entries
# Check  / next as it modifies the following entries
# Handle - next as it is a subrange of values
# Handle * next as it is the whole range of values
# Handle # last as it is a value

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# Takes a cron field with default start/end and expands it to a list of integers
def split(input, start, end):
  output = list()
  mod = None

  # Handle ? as it always exists alone if it does
  if '?' in input:
    return list()

  # Handle , as it combines other entries
  if ',' in input:
    split_vals = input.split(',')
    for i in split_vals:
      test = split(i, start, end)
      output.extend(test)
    return dedupe(output)

  # Handle / next as it modifies sub-entries
  if '/' in input:
    parts = input.split('/')
    mod = int(parts[1])
    input = parts[0]

  # Handle * next as it's the whole range of values
  if '*' in input:
    output = list( range(start, end+1) )
  # Handle - next as it is a subrange of values
  elif '-' in input:
    ends = input.split('-')
    output = list( range(int(ends[0]), int(ends[1])) )
  # Otherwise you a number
  else:
    output.append(int(input))

  if mod is not None:
    mod_output = list()
    for i in output:
      if i % mod == 0:
        mod_output.append(i)
    output = mod_output

  output = set(output)
  return dedupe(output)


def dedupe(input):
  return sorted(set(input), key=int)

# Converts list of integers to space seperated string
def spacify(input):
  output = str()
  for i in input:
    output += f' {i}'
  return output

# Explodes a cron command into a more human-readable format
def cron_parse(input, day_month_to_string=False):
  parts = input.split(" ")

  minutes = split(parts[0], 0, 59)
  hours = split(parts[1], 0, 23)
  month_days = split(parts[2], 1, 31)
  months = split(parts[3], 1, 12)
  week_days = split(parts[4], 0, 7)

  if day_month_to_string:
    months = [ MONTHS[i-1] for i in months ]
    week_days =[ DAYS[i-1] for i in week_days ]
  # Ouput
  print(f'minute        {spacify(minutes)}')
  print(f'hour          {spacify(hours)}')
  print(f'day of month  {spacify(month_days)}')
  print(f'month         {spacify(months)}')
  print(f'day of week   {spacify(week_days)}')
  print(f'command       {parts[5]}')


# Entrypoint into script
def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('input', type=str, help='entire cron command to parse as a string: "0 0 1 * ? /some/command/here"')
  parser.add_argument('--str', dest='day_month_to_string', action='store_true') 
  args = parser.parse_args()
  parts = cron_parse(args.input, args.day_month_to_string)

if __name__ == '__main__':
  main()
