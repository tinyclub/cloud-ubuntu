#!/bin/bash

echo "Username: ubuntu" 
echo "Password: ubuntu" 

(firefox "https://localhost:3000" 2>&1>/dev/null &) 2>&1>/dev/null
