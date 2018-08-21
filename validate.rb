require 'yaml'

begin
  YAML.load_file('./src/reference.yaml')
  puts "OK"
rescue Exception => e
  puts "Failed: #{e.message}"
end
