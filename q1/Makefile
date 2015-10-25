all:	test clean

test:   genlist iplist.txt root.zone
	./common1.py iplist.txt
	./common2.py root.zone

iplist.txt:
	./genlist

root.zone:
	curl -sO http://www.internic.net/zones/root.zone

clean:
	rm -f root.zone iplist.txt
