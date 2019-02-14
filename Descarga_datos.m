% Code for reading data from a private channel
% Since the data is in private channels, the read API Key is needed aside from the channel ID

% Channel ID to read data from
readChannelID1 = 700675;
readChannelID2 = 700676;
% Read API Key
readAPIKey1 = '06JRN81WDRWPNI1U';
readAPIKey2 = 'WH02UUHZXPEDEKKI';

% Read Data
data1 = thingSpeakRead(readChannelID1, 'ReadKey', readAPIKey1,'NumPoints',47,'Fields', [1,2]);
data2 = thingSpeakRead(readChannelID2, 'ReadKey', readAPIKey2,'NumPoints',46,'Fields', [1,2]);

% Merge data from channels 1 and 2 into a single variable 
for i=1:(47+46)
    if mod(i,2)==1
        data(i,:)=data1((i+1)/2,:);
    else
        data(i,:)=data2(i/2,:);
    end
end

data