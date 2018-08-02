#!!AUM!!
from pyfingerprint.pyfingerprint import PyFingerprint
import time

## Tries to initialize the sensor
class fp_class:
    def __init__(self,ttl_path):
        try:
            print ('ttl path ' + ttl_path)
            self.f = PyFingerprint(ttl_path, 57600, 0xFFFFFFFF, 0x00000000)
            if ( self.f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
            ## Gets some sensor information
            print('Currently used templates: ' + str(self.f.getTemplateCount()) +'/'+ str(self.f.getStorageCapacity()))

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
            


    def enrollNgetID(self):
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( self.f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(0x01)

            ## Checks if finger is already enrolled
            result = self.f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                return positionNumber

            print('Remove finger...')
            time.sleep(2)

            print('Waiting for same finger again...')

            ## Wait that finger is read again
            while ( self.f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 2
            self.f.convertImage(0x02)

            ## Compares the charbuffers
            if ( self.f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')
            
            ## Creates a template
            self.f.createTemplate()

            ## Saves template at new position number
            positionNumber = self.f.storeTemplate()
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
            return positionNumber

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            return 0

    def enrollWithID(self,ID_num):
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( self.f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(0x01)

            print('Remove finger...')
            time.sleep(2)

            print('Waiting for same finger again...')

            ## Wait that finger is read again
            while ( self.f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 2
            self.f.convertImage(0x02)

            ## Compares the charbuffers
            if ( self.f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')
            
            ## Creates a template
            self.f.createTemplate()

            ## Saves template at new position number
            positionNumber = self.f.storeTemplate(ID_num)
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
            return positionNumber
            

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))

    

    def CheckFingerPrint(self):
        if self.f.readImage() == False:
            print('Waiting for finger...')
            return (0)
        ## Converts read image to characteristics and stores it in charbuffer 1
        self.f.convertImage(0x01)        
        
        ## Searchs template
        result = self.f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            return(12)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            return(positionNumber)

    def deletfpTemplet(self,positionNumber):
    ## Tries to delete the template of the finger
        try:
            positionNumber = int(positionNumber)
            print('You want to delete: {} Template'.format(positionNumber))
            
            if ( self.f.deleteTemplate(positionNumber) == True ):
                print('Template deleted!')
                
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            return (0)



        

if __name__ == '__main__':
    fp = fp_class('/dev/ttyUSB0')
    fp.deletfpTemplet(1)
    fp.enrollNgetID()
    try:
        while True:
            fp.CheckFingerPrint()
            time.sleep(1)
    except KeyboardInterrupt:
        print ('Project End')






