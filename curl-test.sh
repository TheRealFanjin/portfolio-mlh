res=$(curl --request POST http://127.0.0.1:5000/api/timeline_post -d 'name=testName&email=testEmail&content=testContent')
content=$(echo "$res" | jq -r '.content')
if [ "$content" = "testContent" ]; then
  echo "POST request successfully passed!"
else
  echo "Error in submitting POST request"
fi

res=$(curl http://127.0.0.1:5000/api/timeline_post)
content=$(echo "$res" | jq '.timeline_posts')
if [ "$content" != 'null' ]; then
  echo "GET request successfully passed!"
else
  echo "Error in submitting GET request"
fi