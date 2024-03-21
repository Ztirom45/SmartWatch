touch recived_data.cvs
echo '"accX","accY","accZ"'> recived_data.cvs
unbuffer screen /dev/ttyACM0 | tee -a recived_data.cvs 
