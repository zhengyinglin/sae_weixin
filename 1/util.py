#coding=utf-8
#email  979762787@qq.com
#处理微信请求 (xml 格式)
#http://mp.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E6%8E%A5%E5%8F%A3%E6%8C%87%E5%8D%97

import xml.etree.ElementTree  as ET
import hashlib

def get_signature(token , timestamp , nonce):
    items = [token , timestamp , nonce]
    items.sort()
    return  hashlib.sha1( ''.join(items) ).hexdigest()


class XMLTagText2Dict(object):
    def parse(self, xml_str):
        EL = ET.fromstring(xml_str)
        return self._parse_node(EL)

    def _parse_node(self, node):
        tree = {}
        for child in node:
            ctree = self._parse_node(child)
            value = ctree if ctree else child.text #if child.text else "" 
            name = child.tag

            if name not in tree: # First time found
                tree[name] = value
                continue
            
            val_tree = tree[name]
            if isinstance(val_tree , list):
                val_tree.append(value)
            else:
                tree[name] = [val_tree , value]
        return  tree


class Dict2XMLTagText(object):
    def toxml(self , d , root = 'xml' , indent='  '):
        childs = []
        for k,v in d.items(): #k is string
            if isinstance(v , int):
                childs.append( "%s<%s>%d</%s>" %(indent, k , v , k) )
            elif isinstance(v , basestring ):
                childs.append("%s<%s>%s</%s>" %(indent,k , v , k) )
            elif isinstance(v , dict):
                childs.append( self.toxml(v ,k , indent+'  ')  )
            elif isinstance(v, list):
                items = []
                for v1 in v:
                    items.append( self.toxml(v1 , k , indent+'  ') )
                childs.append( '\n'.join(items) )
            else:
                raise Exception('invalide instance %s' % str(type(v)) )

        return '<%s>\n%s\n</%s>' % (root , '\n'.join(childs) , root)
    
