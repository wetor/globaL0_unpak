import io,os,struct,glob,codecs,math,re
lst='globaL0.pak_list.bin'
hsize=os.path.getsize(lst)
src =lst.replace('_list.bin','')
dirname = src+'_unpacked\\'
src='o_'+src
fl = open(src,'wb+')
filename = os.path.basename(src)
fls=open(lst,'rb')
fl.write(fls.read())
fls.close()
fl.seek(0)

head=bytes('MANAGEDFILE_DATABLOCK_USED_IN_ENGINE_________________________END',encoding='utf-8')
data_pos, = struct.unpack('<I',fl.read(4))
file_num, = struct.unpack('<I',fl.read(4))
postion=data_pos


for i in range(file_num):
    fl.seek(len('FILELINK_____END'),1)
    o_offset = fl.tell()
    fl.read(4)
    o_size=  fl.tell()
    fl.read(4)
    temp, = struct.unpack('B',fl.read(1))
    name=""
    while temp != 0 and temp!= 0x3F:
        name=name+str(chr(temp))
        temp, = struct.unpack('B',fl.read(1))

    name=re.sub(':','_',name)
    name=re.sub('/','\\\\',name)
    
    pos=fl.tell()
    size=os.path.getsize(dirname+name)
    
    fl.seek(o_offset)
    fl.write(struct.pack('<I',postion-data_pos))
    fl.write(struct.pack('<I',size))
    fl.seek(postion)
    fl.write(head)
    print(i,postion,size,name)
    file=open(dirname+name,'rb')
    fl.write(file.read())
    file.close()
    
    postion=postion+size+0x40
    
    fl.seek(pos)
    
    
    
    temp, = struct.unpack('B',fl.read(1))
    while temp!=0x46 and fl.tell()<hsize :
        temp, = struct.unpack('B',fl.read(1))
    fl.seek(-1,1)

fl.close()

