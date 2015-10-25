all:	test clean

test:   genlist iplist.txt root.zone
	./common1.py iplist.txt
	./common2.py root.zone

iplist.txt:
	./genlist

root.zone:
	curl -sO ftp://rs.internic.net/domain/root.zone

clean:
	rm root.zone iplist.txt
