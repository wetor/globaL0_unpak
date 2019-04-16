import io,os,struct,glob,codecs,math,re
src = 'globaL0.pak'

fl = open(src,'rb')
filename = os.path.basename(src)
fls=open(src+'_list.txt','w')
flh=open(src+'_list.bin','wb')
data_pos, = struct.unpack('<I',fl.read(4))
fl.seek(0)
flh.write(fl.read(data_pos))
fl.seek(4)
file_num, = struct.unpack('<I',fl.read(4))
fls.write(str(file_num)+'\n')
#file_num=10
print(file_num,data_pos)
for i in range(file_num):
    fl.seek(len('FILELINK_____END'),1)
    offset, = struct.unpack('<I',fl.read(4))
    size, = struct.unpack('<I',fl.read(4))
    temp, = struct.unpack('B',fl.read(1))
    name=""
    while temp != 0 and temp!= 0x3F:
        name=name+str(chr(temp))
        temp, = struct.unpack('B',fl.read(1))
    name=re.sub(':','_',name)
    name=re.sub('/','\\\\',name)
    fls.write(str(i)+','+name+"\n")
    dirname = os.path.dirname(name)
    if os.path.isdir(filename+'_unpacked\\'+dirname) == False:
        os.makedirs(filename+'_unpacked\\'+dirname)
    old = open(filename+'_unpacked\\'+name,'wb')
    pos=fl.tell()
    fl.seek(data_pos+offset+0x40)
    old.write(fl.read(size))
    old.close()
    fl.seek(pos)
    
    print(i,data_pos+offset,size,name)
    
    
    temp, = struct.unpack('B',fl.read(1))
    while temp!=0x46 :
        temp, = struct.unpack('B',fl.read(1))
    fl.seek(-1,1)
fl.close()
fls.close()
flh.close()
