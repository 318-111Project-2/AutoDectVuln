cp app/configs/config.py.template app/configs/config.py
SECRET_KEY=`openssl rand -base64 32`
sed -i "s-SECRET_KEY = '.*'-SECRET_KEY = '$SECRET_KEY'-" app/configs/config.py
